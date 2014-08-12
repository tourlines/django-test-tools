# coding: utf-8
from django.test import TestCase


class ObjectWithFieldBaseTestCase(TestCase):

    __is_custom_field = False

    @property
    def SETTINGS_CONSTANT_NAME(self):
        raise NotImplementedError(
            'Defina uma constante com o nome da variável que armazena as '
            'funções que validam fields extras (não padrões do django)')

    @property
    def SETTINGS_CONSTANT(self):
        from django.conf import settings
        try:
            retorno = getattr(settings, self.SETTINGS_CONSTANT_NAME)
        except AttributeError:
            retorno = None

        return retorno

    @property
    def BUILT_IN_FIELDS(self):
        """
        Local onde ficam os fields padrões do objeto em questão.
        Quando falamos de fields de models (CharField, DateField)
        o local padrão deles é o models dentro de django.db.
        """
        raise NotImplementedError(
            'Informe na variável BUILT_IN_FIELDS o local onde ficam os fields '
            'padrões do objeto em questão!'
        )

    @property
    def FIELD_VALIDATORS(self):
        """
        Cada field pode possuir validadores unicos, para checar opções
        próprias ou até mesmo dependencias do field e portanto cada um
        deve ter uma função validadora que irá fazer estas checagens.
        A função deve seguir o padrão field_<<nomedofield>>
        """
        raise NotImplementedError(
            'Informe o modulo onde se encontram os validadores dos fields!')

    @property
    def OPTION_VALIDATORS(self):
        """
        Normalmente as opções gerais de todos os fields são simples de
        validar, apenas um assertEqual já é o suficiente. Mas em casos
        mais complexos isto não é verdade. Antes de fazer a validação
        da opção é feita uma busca dentro do modulo validador de
        opções se existe uma função para validar a mesma, caso
        contrario ele segue com o assertEqual básico
        """
        raise NotImplementedError(
            'Informe o modulo que estão as funções validadoras de opções!')

    def get_atributo(self, nome):
        raise NotImplementedError(
            'Dado um nome esta função retorna o campo do objeto '
            'correspondente ao mesmo')

    def _get_atributo_no_objeto(self, nome, objeto):
        """
        Verifica e retorna, caso exista o atributo desejado dentro do
        objeto sobre teste
        """
        try:
            campo = self.get_atributo(nome)
        except NameError:
            self.fail('Não existe nenhum atributo com o nome "%s" no "%s"' % (
                nome, objeto))

        return campo

    def _get_field(self, field):
        """
        Retorna a classe que representa o field do atributo.

        Para deixar o código mais limpo é permitido que o usuário
        passe apenas o nome do field (sem precisar importar ele), caso
        seja um field padrão do django ele será importado e retornado.

        TODO: Caso o field não seja padrão do django o usuário
        infelizmente terá que importar o field e passar ele como
        parametro. Talvez deva-se implementar uma variável onde o
        mesmo possa registrar seus fields
        """
        if isinstance(field, basestring):
            try:
                field = getattr(self.BUILT_IN_FIELDS, field)
            except AttributeError:
                raise AttributeError(
                    'O field "%s" não é padrão do django e nestes ' % field,
                    'casos não é permitido referenciar ele apenas pelo nome. '
                    'Importe o field e o passe diretamente.')
        else:
            self.__is_custom_field = True

        return field

    def _validar_field_options(self, campo, field, options, **kwargs):
        """
        Valida as opções especificas de cada field

        Fields normalmente possuem opções que são especificas para
        cada um deles (como a opção max_length), e as vezes o field
        pode mudar o funcionamento as opções padrões. O DateField, é
        um exemplo, quando a opção auto_now esta habilitada ele
        automaticamente coloca a opção blank do field igual a true
        (isto sem o concentimento do usuário) e portanto precisamos
        fazer esta validação
        """
        from copy import deepcopy

        # Valida as opções implementadas pelo proprio field
        field_options = deepcopy(kwargs)

        for option in options:
            if option.nome in field_options:
                del(field_options[option.nome])

        if self.SETTINGS_CONSTANT:
            funcao_validadora = self.SETTINGS_CONSTANT.get(field.__name__)

        if not self.SETTINGS_CONSTANT or not funcao_validadora:
            try:
                funcao_validadora = getattr(
                    self.FIELD_VALIDATORS, 'field_%s' % field.__name__.lower())
            except AttributeError as e:
                if not self.__is_custom_field:
                    raise e
                else:
                    print "WARING: Skipping all tests for field %s" % field
                    return []

        return funcao_validadora(self, campo, **field_options) or []

    def base_validar_field(self, nome, field, objeto, options, **kwargs):
        campo = self._get_atributo_no_objeto(nome, objeto)
        field = self._get_field(field)

        self.assertEqual(campo.__class__, field, (
            'O atributo "%s" não é do tipo "%s"' % (nome, field)))

        opcoes_validadas = \
            self._validar_field_options(campo, field, options, **kwargs)

        for option in options:

            if not option.e_compativel_django() or \
                    option.nome in opcoes_validadas:
                continue

            try:
                getattr(self.OPTION_VALIDATORS, 'option_%s' % option.nome)(
                    self, campo, nome, **kwargs)
            except (AttributeError, TypeError):
                pass
            else:
                continue

            field_option = getattr(campo, option.nome)
            # Este if poderia ser escrito com um simples "valor = kwargs.get(
            # option.nome) or option.default". Contudo a seguinte lógica
            # impede que isto possa ser feito: o default de um Boolean pode ser
            # false e isto faria com que o python ignorasse o argumento default
            # dos kwargs e portanto mesmo que o usuário informasse que é false
            # ele iria buscar o valor padrão da opção.
            if option.nome in kwargs:
                valor = kwargs[option.nome]
            else:
                valor = option.default

            self.assertEqual(
                field_option, valor,
                'Opção "%s" do field "%s" deveria ser "%s", mas é "%s"' % (
                    option.nome, nome, valor, field_option
                )
            )

    def validar_field(self, nome, field, **kwargs):
        raise NotImplementedError

    def validar(self):
        raise NotImplementedError

    def test_validar_objetos(self, nome_classe='ObjectWithFieldBaseTestCase'):
        if not self.__class__.__name__ == nome_classe:
            self.validar()
        else:
            pass
