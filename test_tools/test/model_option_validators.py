# coding: utf-8
from django.db.models.fields import NOT_PROVIDED
from ..faults import TestAssertionError


NOT_PROVIDED_HELP_TEXT = u''


def option_error_messages(
        self, campo, nome, error_messages=NOT_PROVIDED, **kwargs):
    if error_messages != NOT_PROVIDED:
        self.fail('Não foi implementado testes para esta opção.')


def option_validators(
        self, campo, nome, validators=NOT_PROVIDED, **kwargs):
    if validators != NOT_PROVIDED:
        self.fail('Não foi implementado testes para esta opção.')


def option_choices(self, campo, nome, choices, **kwargs):

    # Acrecenta o nome da classe com um 's' caso o mesmo já não esteja
    nome_classe = nome if nome[len(nome) - 1] == 's' else '%ss' % nome
    nome_constante = '%s_CHOICES' % nome_classe.upper()

    try:
        constante = getattr(self.model, nome_constante)
    except AttributeError:
        raise TestAssertionError(
            (
                'Não foi definida a constante %s para o campo %s dentro do'
                'model'
            ) % (nome_constante, nome, self.model)
        )

    self.assertEqual(
        campo.choices, constante,
        (
            'A opção choices do campo %s não esta apontado para a '
            'variável correta "%s"'
        ) % (nome, nome_constante)
    )

    self.assertEqual(len(constante), len(choices), (
        'A constante choices do campo %s é diferente do desejado' % nome
    ))

    for choice in choices:
        if isinstance(choice, list):
            verbose = choice[1]
            choice = choice[0]
        else:
            verbose = choice

        try:
            valor_choice = getattr(
                getattr(self.model, nome_classe.title()),
                '%s' % choice.upper().replace(' ', '_')
            )
        except AttributeError:
            raise TestAssertionError(
                (
                    'A o valor desejado %s para a constante %s não foi '
                    'definido na sua classe "%s"'
                ) % (
                    choice.upper().replace(' ', '_'), nome_constante,
                    nome_classe)
            )

        self.assertTrue(dict(constante).get(valor_choice), (
            'A constante choices %s do campo %s não esta usando as '
            'definições da classe %s') % (
            nome_constante, nome, nome_classe)
        )

        self.assertEqual(dict(constante)[valor_choice], verbose, (
            'Os nomes verbose na constante %s não estão corretos') %
            nome_constante
        )


def option_verbose_name(
        self, campo, nome, verbose_name='', **kwargs):
    """
    Valida a valor da opção verbose_name

    O usuário deve possuir o direito de escolher que nível de
    validação ele deseja chegar. Neste caso é possivel que a
    variável assuma 3 valores.

        - [verbose_name = None]: é esperado que o verbose_name do
    field assuma o valor padrão, que é o proprio nome do field
        - [verbose_name = True]: ele asssume que o verbose_name
    não é o padrão do django (foi modificado pelo usuário) mas o
    mesmo não deseja fazer uma validação muito detalhada sobre o
    ele, ou seja não é um bit significativo :D
        - [verbose_name = <<string>> ]: neste caso será verificado
    se o campo possui o texto exatamanto fornecido pelo usuário.
    Em outras palavras o texto é de grande importância para o
    funcionamento do sistema.
    """

    if not verbose_name:
        self.assertEqual(
            campo.verbose_name, unicode(nome.replace('_', ' ')))
    elif verbose_name is True:
        self.assertNotEqual(
            campo.verbose_name, unicode(nome.replace('_', ' ')))
    elif isinstance(verbose_name, basestring):
        self.assertEqual(campo.verbose_name, unicode(verbose_name))
    else:
        self.fail(
            'O valor do verbose_name passado não é válido: "%s"' % (
                verbose_name))


def option_help_text(
        self, campo, nome, help_text=NOT_PROVIDED_HELP_TEXT, **kwargs):
    """
    SEE: self.option_verbose_name.__docstring__
    """
    if not help_text:
        self.assertEqual(campo.help_text, help_text)
    elif help_text is True:
        self.assertNotEqual(campo.help_text, NOT_PROVIDED_HELP_TEXT)
    elif isinstance(help_text, basestring):
        self.assertEqual(campo.help_text, unicode(help_text))
    else:
        self.fail(
            'O valor do help_text passado não é válido: "%s"' % (
                help_text))
