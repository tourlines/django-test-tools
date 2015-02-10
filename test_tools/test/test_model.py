# coding: utf-8
from django.db.models.fields import NOT_PROVIDED
from .test_base import ObjectWithFieldBaseTestCase
from . import (
    model_field_validators, model_option_validators, model_meta_validators)
from ..utils import Option, camelcase_to
from django.db import models
from .model_option_validators import NOT_PROVIDED_HELP_TEXT


class ModelTestCase(ObjectWithFieldBaseTestCase):

    SETTINGS_CONSTANT_NAME = 'TEST_MODEL_FIELD_VALIDATORS'
    BUILT_IN_FIELDS = models
    FIELD_VALIDATORS = model_field_validators
    OPTION_VALIDATORS = model_option_validators
    META_VALIDATORS = model_meta_validators

    @property
    def model(self):
        raise NotImplementedError(
            'Defina qual model deseja testar criando uma variável na classe '
            'seguindo o exemplo:\n'
            '    model = <<MeuModel>>')

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
                versao_minima=(1, 8, 0)),
            Option('get_latest_by', None),
            Option('managed', True),
            Option('order_with_respect_to', None),
            Option('ordering', []),
            Option('permissions', []),
            Option('default_permissions',
                   ('add', 'change', 'delete'),
                   versao_minima=(1, 7, 0)),
            Option('proxy', False),
            Option('select_on_save', False, versao_minima=(1, 6, 0)),
            Option('unique_together', ()),
            Option('index_together', ()),
            Option('verbose_name', camelcase_to(
                self.model.__name__, space=True)),
            Option('verbose_name_plural', '')
        ]

        super(ModelTestCase, self).base_validar_meta(
            self.model, OPTIONS, **kwargs)

    def test_validar_objetos(self):
        super(ModelTestCase, self).test_validar_objetos(
            nome_classe='ModelTestCase')


class CMSPluginModelTestCase(ModelTestCase):

    def validar(self):
        from cms.models.pluginmodel import CMSPlugin

        super(CMSPluginModelTestCase, self).validar()
        self.assertTrue(issubclass(self.model, CMSPlugin), (
            'O model %s não herda de CMSPlugin e por definição do CMS todos '
            'os models de plugin devem herdar desta classe'))

    def test_validar_objetos(self):
        super(ModelTestCase, self).test_validar_objetos(
            nome_classe='CMSPluginModelTestCase')
