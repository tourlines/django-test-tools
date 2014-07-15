# coding: utf-8


class Option(object):

    nome = ''
    default = ''
    versao_minima = ()

    def __init__(self, nome, default, versao_minima=(0, 0, 0, '', 0)):
        self.nome = nome
        self.default = default
        self.versao_minima = versao_minima

    def e_compativel_django(self):
        from django import VERSION

        if VERSION[0] > self.versao_minima[0]:
            return True
        elif VERSION[0] == self.versao_minima[0]:
            if VERSION[1] > self.versao_minima[1]:
                return True
            elif VERSION[1] == self.versao_minima[1]:
                if VERSION[2] >= self.versao_minima[2]:
                    return True

        return False

    def __str__(self):
        return '%s' % self.nome

    def __repr__(self):
        return self.__str__()


def camelcase_to(texto, underscore=False, space=False):
    """
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
