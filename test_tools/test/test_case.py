# coding: utf-8
from django.test import TestCase as DjangoBaseTestCase
from unittest import TestCase as UnittestBaseTestCase


class _AssertRaisesContext(object):
    """
    Esta é uma cópia da implementação do '_AssertRaisesContext' de
    forma integral pelo fato da mesma ser na teoria uma classe
    privada e por isto não pode ser acessada.

    SEE: unittest.case.__AssertRaisesContext
    """

    def __init__(self, expected, test_case, expected_regexp=None, msg=''):
        """
        NOTE: Adicionado um argumento "msg" para que seja possivel
        armazenar qual mensagem o usuário deseja exibir
        """
        self.expected = expected
        self.failureException = test_case.failureException
        self.expected_regexp = expected_regexp
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """
        NOTA: foi adicionado um "if" no momento da chamada da exceção
        """
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            # Nesta etapa ele checa se o atributo "msg" foi definido e se sim
            # exibe a mensagem armazenada no mesmo, caso contrario apenas 
            # segue o fluxo padrão da classe
            if self.msg:
                raise self.failureException(self.msg)
            else:
                raise self.failureException(
                    "{0} not raised".format(exc_name))
        if not issubclass(exc_type, self.expected):
            return False
        self.exception = exc_value
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('"%s" does not match "%s"' %
                     (expected_regexp.pattern, str(exc_value)))
        return True


class TestCaseBase(object):

    def assertRaisesWithMsg(
            self, excClass, callableObj=None, msg='', *args, **kwargs):
        """
        Esta é uma reimplemetação do assertRaises para permitir que
        seja customizado a mensagem que é exibida quando a exceção
        é chamada
        """
        context = _AssertRaisesContext(excClass, self, msg=msg)
        if callableObj is None:
            return context
        with context:
            callableObj(*args, **kwargs)


class DjangoTestCase(TestCaseBase, DjangoBaseTestCase):
    pass


class UnittestTestCase(TestCaseBase, UnittestBaseTestCase):
    pass
