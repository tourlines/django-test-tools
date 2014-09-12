# coding: utf-8
from django.forms import fields
from .test_base import ObjectWithFieldBaseTestCase
from . import (
    form_field_validators, form_option_validators, form_meta_validators)
from ..utils import Option


class FormTestCase(ObjectWithFieldBaseTestCase):

    SETTINGS_CONSTANT_NAME = 'TEST_FORM_FIELD_VALIDATORS'
    BUILT_IN_FIELDS = fields
    FIELD_VALIDATORS = form_field_validators
    OPTION_VALIDATORS = form_option_validators
    META_VALIDATORS = form_meta_validators

    def get_atributo(self, nome):
        return self.form.base_fields[nome]

    @property
    def form(self):
        raise NotImplementedError(
            'Defina qual model deseja testar criando uma variável na classe '
            'seguindo o exemplo:\n'
            '    form = <<MeuForm>>')

    def validar_field(self, nome, field, **kwargs):
        OPTIONS = [
            Option('widget', None),
        ]

        self.base_validar_field(nome, field, self.form, OPTIONS, **kwargs)

    def validar_meta(self, **kwargs):
        OPTIONS = [
            Option('fields', []),
        ]

        # Verica se o form possui meta implementado
        if getattr(self.form, 'Meta', ''):
            self.base_validar_meta(self.form, OPTIONS, **kwargs)

    def test_validar_objetos(self):
        super(FormTestCase, self).test_validar_objetos(
            nome_classe='FormTestCase')
