# coding: utf-8
from cms.models.pluginmodel import CMSPlugin
from django.test import TestCase


class CMSPluginTestCase(TestCase):
    """
    Devido ao bug descrito na função get_plugin qualquer classe que
    herde deste TestCase deve implementar uma função get_plugin
    informando onde fica o seu modulo de plugins principal.

    SEE: get_plugin & get_plugin_ docstrings
    """

    __plugin = None
    validar_nome_model = True
    validar_local_template = True
    nome_app = ''
    PULAR_TESTES_CLASSE = 'CMSPluginTestCase'

    @property
    def plugin(self):
        raise NotImplementedError(
            'Informe o nome ou o proprio plugin que esta sendo testado na '
            'variável "plugin"')

    @property
    def atributos(self):
        raise NotImplementedError(
            'Informe os valores dos campos definidos no plugin em um '
            'dicionario igual a: atributos: {model: Model, name=NamePlugin}')

    def get_plugin_(self, cms_plugins_module):
        """
        Função criada somente para propor uma solução alternativa ao
        bug descrito da função 'get_plugin'.

        SEE: docstring da classe
        """

        if not self.__plugin:
            if isinstance(self.plugin, basestring):
                self.__plugin = getattr(cms_plugins_module, self.plugin)
            else:
                self.__plugin = self.plugin

        return self.__plugin

    def get_plugin(self):
        """
        Retorna a classe do plugin atravéz do nome da mesma

        NOTA: Esta função deveria fazer um simples getattr dentro do
        arquivo onde ficam definido os plugins. Contudo devido a um
        problema de importe circular isto não é possivel. Além disto
        cada app pode ter seu modulo de cms_plugins distinto. Para
        cada função que herda deste TestCase ele deve dizer a onde
        estão os plugins da app.

            EX:
                from app import cms_plugins

                return self.get_plugin_(cms_plugins)
        """
        raise NotImplementedError('Diga em qual modulo esta o seus plugins!')

    def test_nome_model(self, pular_classe='CMSPluginTestCase'):
        if self.__class__.__name__ == pular_classe or \
                not self.validar_nome_model:
            return

        esperado = '%sModel' % self.get_plugin().__name__
        definido = self.get_plugin().model.__name__

        self.assertEqual(
            definido, esperado, (
                'Siga o padrão do projeto: o nome do model do plugin deve '
                'ser %s mas foi definido como %s' % (esperado, definido)
            ))

    def camelcase_to(self, texto, underscore=False, space=False):
        """
        Converte uma string em CamelCase para underscore ou espaços

        THANKS: http://stackoverflow.com/questions/1175208/elegant-python-
        function-to-convert-camelcase-to-camel-case
        """
        import re

        if underscore:
            novo = r'\1_\2'
        elif space:
            novo = r'\1 \2'
        else:
            raise AttributeError('É preciso que underscore ou space seja True')

        novo_texto = re.sub('(.)([A-Z][a-z]+)', novo, texto)

        return re.sub('([a-z0-9])([A-Z])', novo, novo_texto).lower()

    def test_local_template(
            self, template_middle='', pular_classe='CMSPluginTestCase'):
        if self.__class__.__name__ == pular_classe or \
                not self.validar_local_template:
            return

        definido = self.get_plugin().render_template
        # Quando um plugin não possui model o django CMS linka o plugin ao
        # model padrão dele - CMSPlugin. E por isto o nome da app é colocada
        # automaticamente como "cms". Nestes casos deve haver a possibilidade
        # de fornecer qual o nome da app.
        esperado = '%s/%s%s.html' % (
            self.nome_app or self.get_plugin().model._meta.app_label,
            template_middle,
            self.camelcase_to(
                self.get_plugin().__name__.split('Plugin')[0], underscore=True)
        )

        self.assertEqual(
            definido, esperado, (
                'Siga o padrão do projeto: o local do template  deve '
                'ser %s mas foi definido como %s' % (esperado, definido)
            ))

    def _validar_plugin(
            self, name, allow_children=False, child_classes=None,
            model=CMSPlugin, render_template='', filter_horizontal=(),
            exclude=(), require_parent=False, parent_classes=None,
            module=None):

        self.assertEqual(self.get_plugin().name, name, (
            'O nome %s é diferente de %s' % (
                self.get_plugin().name[0:], name[0:])))
        self.assertEqual(self.get_plugin().allow_children, allow_children)
        self.assertEqual(self.get_plugin().child_classes, child_classes)
        self.assertEqual(self.get_plugin().require_parent, require_parent)
        self.assertEqual(self.get_plugin().parent_classes, parent_classes)
        self.assertEqual(
            self.get_plugin().filter_horizontal, filter_horizontal)

        # HACK: De alguma forma ele gera um objeto do tipo proxy, que é
        # importável.
        if module:
            self.assertEqual(self.get_plugin().module, module)
        if not module:
            self.assertEqual(
                self.get_plugin().module.__class__.__name__, '__proxy__')

        if not self.validar_nome_model:
            self.assertEqual(self.get_plugin().model, model)

        if not self.validar_local_template:
            self.assertEqual(
                self.get_plugin().render_template, render_template)

    def test_validar_plugin(self, pular_classe='CMSPluginTestCase'):
        if self.__class__.__name__ == pular_classe:
            return

        self._validar_plugin(**self.atributos)
