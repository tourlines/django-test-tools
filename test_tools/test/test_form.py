# coding: utf-8
from django.forms import fields
from .test_base import ObjectWithFieldBaseTestCase
from . import form_field_validators, form_option_validators


class FormTestCase(ObjectWithFieldBaseTestCase):

    SETTINGS_CONSTANT_NAME = 'TEST_FORM_FIELD_VALIDATORS'
    BUILT_IN_FIELDS = fields
    FIELD_VALIDATORS = form_field_validators
    OPTION_VALIDATORS = form_option_validators

    def get_atributo(self, nome):
        return self.form.base_fields[nome]

    @property
    def form(self):
        raise NotImplementedError(
            'Defina qual model deseja testar criando uma variável na classe '
            'seguindo o exemplo:\n'
            '    form = <<MeuForm>>')

    @property
    def campos(self):
        raise NotImplementedError(
            'Crie uma lista de dicionario contendo a relação dos campos do '
            'model a ser testado. Exemplo (Veja a docstring para mais '
            'detalhes):\n'
            '    campos = [{'
            '         "nome": "nome_campo",'
            '         "tipo": CharField')

    def validar_field(self, nome, tipo):
        super(FormTestCase, self).base_validar_field(nome, tipo, self.form, [])

    def validar(self):
        for campo in self.campos:
            self.validar_field(**campo)
