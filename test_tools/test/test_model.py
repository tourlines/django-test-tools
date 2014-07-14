# coding: utf-8
from django.db.models.fields import NOT_PROVIDED
from django.test import TestCase
from ..utils import Option, camelcase_to


NOT_PROVIDED_HELP_TEXT = u''


class ModelTestCase(TestCase):

    @property
    def model(self):
        raise NotImplementedError(
            'Defina qual model deseja testar criando uma variável na classe '
            'seguindo o exemplo:\n'
            '    model = <<MeuModel>>')

    @property
    def campos(self):
        raise NotImplementedError(
            'Crie uma lista de dicionario contendo a relação dos campos do '
            'model a ser testado. Exemplo (Veja a docstring para mais '
            'detalhes):\n'
            '    campos = [{'
            '         "nome": "nome_campo",'
            '         "tipo": CharField,'
            '         "max_length": 32}]')

    @property
    def meta(self):
        raise NotImplementedError(
            'Crie um dicionario contento todos os itens to meta seguindo o '
            'exemplo:\n'
            '    meta = {"ordering": ("campo",),}')

    def validar_field(self, nome, tipo, **kwargs):
        from django.db import models
        from django.conf import settings
        from . import field_validators, option_validators

        OPTIONS = [
            Option('null', False),
            Option('blank', False),
            Option('choices', []),
            Option('db_column', None),
            Option('db_index', False),
            Option('db_tablespace', settings.DEFAULT_INDEX_TABLESPACE),
            Option('default', NOT_PROVIDED),
            Option('editable', True),
            Option('error_messages', {}),
            Option('help_text', NOT_PROVIDED_HELP_TEXT),
            Option('primary_key', False),
            Option('unique', False),
            Option('unique_for_date', None),
            Option('unique_for_month', None),
            Option('unique_for_year', None),
            Option('verbose_name', ''),
            Option('validators', []),
        ]

        try:
            campo = self.model._meta.get_field(nome)
        except NameError:
            self.fail('Não existe nenhum campo no model com o nome %s' % nome)

        if isinstance(tipo, basestring):
            try:
                tipo = getattr(models, tipo)
            except AttributeError:
                raise AttributeError(
                    'O field "%s" não é padrão do django e nestes ' % tipo,
                    'casos não é permitido referenciar ele apenas pelo nome. '
                    'Importe ele e o passe como parametro no tipo no lugar de '
                    'informar seu nome')

        self.assertEqual(campo.__class__, tipo, (
            'O campo %s não é do tipo %s' % (nome, tipo)))

        if 'TEST_TOOLS_FIELD_VALIDATORS' in dir(settings) and \
                tipo.__name__ in settings.TEST_TOOLS_VALIDATORS:
            validacoes_feitas = \
                settings.TEST_TOOLS_VALIDATORS[tipo.__name__](
                    self, campo, **kwargs)
        else:
            validacoes_feitas = \
                getattr(field_validators, 'field_%s' % tipo.__name__.lower())(
                    self, campo, **kwargs)

        for option in OPTIONS:

            # Alguns fields possuem validações nas opções padrões do field base
            # caso esta opção tenha sido validada dentro do field não devemos
            # fazer a sua revalidação aqui
            if not option.e_compativel_django() or validacoes_feitas and \
                    option.nome in validacoes_feitas:
                continue

            # Algumas opções podem ter validações um pouco mais avançadas e
            # caso esta seja uma delas irá chamar a função que irá fazer a
            # validação.
            # As funções seguem o padrão: def _validar_option_<<nome_da_opcao>>
            try:
                getattr(option_validators, 'option_%s' % option.nome)(
                    self, campo, nome, **kwargs)
            except (AttributeError, TypeError):
                pass
            else:
                continue

            # Caso a opção não tenha sido testada e nem exista uma função para
            # fazer sua validação de forma avançada será feita uma siples
            # validação de igualdade. Neste caso ele verifica se o usuário
            # definiu algum valor para a opção, caso contrario busca o seu
            # valor padrão e assim procede com a validação
            valor = kwargs.get(option.nome) or option.default
            field_option = getattr(campo, option.nome)
            self.assertEqual(
                field_option, valor,
                'Opção %s do field %s deveria ser %s, mas é %s' % (
                    option.nome, nome, valor, field_option
                )
            )

    def validar_meta(self, **kwargs):
        from django.conf import settings
        from . import meta_validators

        # FIXME: Atualmente quando a pessoa não passa o app_label ele é
        # obtido através do proprio model, isto é a mesma coisa que não testar
        OPTIONS = [
            Option('abstract', False),
            Option('app_label', self.model._meta.app_label),
            Option('db_table', '%s_%s' % (
                self.model._meta.app_label,
                self.model.__name__.lower())),
            Option('db_tablespace', settings.DEFAULT_TABLESPACE),
            Option('default_related_name', '%s_set' % (
                camelcase_to(self.model.__name__, underscore=True)),
                versao_minima=(1, 7, 0)),
            Option('get_latest_by', None),
            Option('managed', True),
            Option('order_with_respect_to', None),
            Option('ordering', []),
            Option('permissions', []),
            Option('default_permissions', (), versao_minima=(1, 7, 0)),
            Option('proxy', False),
            Option('select_on_save', False, versao_minima=(1, 6, 0)),
            Option('unique_together', []),
            Option('index_together', []),
            Option('verbose_name', camelcase_to(
                self.model.__name__, space=True)),
            Option('verbose_name_plural', '')
        ]

        for option in OPTIONS:
            if option.e_compativel_django():

                # Algumas opções do meta, assim como dos fields, podem ter
                # validações um pouco mais avançadas e devemos usar funções
                # para isto
                # As funções seguem o padrão: def _validar_meta_option_
                # <<nome_da_opcao>>
                try:
                    getattr(meta_validators, 'meta_%s' % option.nome)(
                        self, **kwargs)
                except (AttributeError, TypeError):
                    pass
                else:
                    continue

                valor = kwargs.get(option.nome) or option.default
                meta_option = getattr(self.model._meta, option.nome)
                self.assertEqual(
                    meta_option, valor, 'Opção %s deveria ser %s, mas é %s' % (
                        option.nome, valor, meta_option
                    )
                )

    def validar(self):
        for campo in self.campos:
            self.validar_field(**campo)

        self.validar_meta(**self.meta)
