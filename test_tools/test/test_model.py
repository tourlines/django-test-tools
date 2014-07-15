# coding: utf-8
from django.db.models.fields import NOT_PROVIDED
from .test_base import ObjectWithFieldBaseTestCase
from . import model_field_validators, model_option_validators
from ..utils import Option, camelcase_to
from django.db import models
from .model_option_validators import NOT_PROVIDED_HELP_TEXT


class ModelTestCase(ObjectWithFieldBaseTestCase):

    SETTINGS_CONSTANT_NAME = 'TEST_MODEL_FIELD_VALIDATORS'
    BUILT_IN_FIELDS = models
    FIELD_VALIDATORS = model_field_validators
    OPTION_VALIDATORS = model_option_validators

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

    def get_atributo(self, nome):
        return self.model._meta.get_field(nome)

    def validar_field(self, nome, field, **kwargs):
        from django.conf import settings

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

        super(ModelTestCase, self).base_validar_field(
            nome, field, self.model, OPTIONS, **kwargs)

    def validar_meta(self, **kwargs):
        from django.conf import settings
        from . import model_meta_validators

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
                    getattr(model_meta_validators, 'meta_%s' % option.nome)(
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

    def test_validar_objetos(self):
        super(ModelTestCase, self).test_validar_objetos(
            nome_classe='ModelTestCase')
