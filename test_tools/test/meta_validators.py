# coding: utf-8


def meta_verbose_name_plural(self, **kwargs):
    """
    TODO: É preciso entender o funcionamento do valor padrão da
    opção verbose_name_plural, aparentemente o valor do model é
    uma classe do tipo proxy que aponta para algo desconhecido
    """
    if kwargs.get('verbose_name_plural'):
        self.assertEqual(
            self.model._meta.verbose_name_plural,
            kwargs['verbose_name_plural'])
    else:
        self.assertEqual(
            self.model._meta.verbose_name_plural.__class__.__name__,
            '__proxy__')
