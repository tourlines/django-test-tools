# coding: utf-8
from django.test import TestCase


class FormTestCase(TestCase):

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
        from django.forms import fields

        try:
            field = self.form.base_fields[nome]
        except KeyError:
            self.fail('Não existe o campo %s dentro do form %s' % (
                nome, self.form))

        if isinstance(tipo, basestring):
            try:
                tipo = getattr(fields, tipo)
            except AttributeError:
                raise AttributeError(
                    'O field "%s" não é padrão do django e nestes ' % tipo,
                    'casos não é permitido referenciar ele apenas pelo nome. '
                    'Importe ele e o passe como parametro no tipo no lugar de '
                    'informar seu nome')

        self.assertEqual(field.__class__, tipo, (
            'O field %s não é do tipo %s' % (nome, tipo)))

    def validar(self):
        for campo in self.campos:
            self.validar_field(**campo)
