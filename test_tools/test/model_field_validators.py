# coding: utf-8
from django.db.models.fields import NOT_PROVIDED


def field_autofield(self, campo):
    self.assertTrue(campo.primary_key)

    return ['primary_key']


def field_bigintegerfield(self, campo):
    pass


def field_binaryfield(self, campo):
    pass


def field_booleanfield(self, campo):
    pass


def field_charfield(self, campo, max_length):
    self.assertEqual(campo.max_length, max_length)


def field_commaseparatedintegerfield(self, campo, max_length):
    self.assertEqual(campo.max_length, max_length)


def field_datefield(
        self, campo, auto_now=False, auto_now_add=False):
    self.assertEqual(campo.auto_now, auto_now)
    self.assertEqual(campo.auto_now_add, auto_now_add)

    if auto_now or auto_now_add:
        self.assertTrue(campo.blank)
        self.assertFalse(campo.editable)

        return ['blank', 'editable']


def field_datetimefield(self, campo, **kwargs):
    return field_datefield(self, campo, **kwargs)


def field_decimalfield(self, campo, max_digits, decimal_places):
    self.assertEqual(campo.max_digits, max_digits)
    self.assertEqual(campo.decimal_places, decimal_places)


def field_emailfield(self, campo, max_length=NOT_PROVIDED):
    from django import VERSION

    # NOTE: O campo max_length foi aumentado de tamanho no django para
    # seguir os padrões internecionais, contudo esta modificação foi feita
    # apenas em desenvolvimento. Até a versão 1.7.1 ainda não foi liberada
    # SEE: docs.djangoproject.com/en/dev/ref/models/fields/#emailfield
    if max_length == NOT_PROVIDED:
        if VERSION[1] == 7 and VERSION[4] > 1:
            max_length = 254
        else:
            max_length = 75

    self.assertEqual(campo.max_length, max_length)


def field_filefield(
        self, campo, upload_to=None, max_length=100):
    from django import VERSION

    # SEE: docs.djangoproject.com/en/dev/ref/models/fields/#django.db.
    # models.FileField.upload_to
    if not upload_to and VERSION[1] == 7:
        raise TypeError(
            'O argumento upload_to é requirido nas versões do django '
            'anteriores a 1.7')

    self.assertEqual(campo.upload_to, upload_to)
    self.assertEqual(campo.max_length, max_length)


def field_filepathfield(
        self, campo, path, match=None, recursive=False, allow_files=False,
        allow_folders=False, max_length=100):
    self.assertEqual(campo.path, path)
    self.assertEqual(campo.match, match)
    self.assertEqual(campo.recursive, recursive)
    self.assertEqual(campo.allow_files, allow_files)
    self.assertEqual(campo.allow_folders, allow_folders)
    self.assertEqual(campo.max_length, max_length)


def field_floatfield(self, campo):
    pass


def field_imagefield(
        self, campo, upload_to=None, height_field=None, width_field=None,
        max_length=100):
    self.assertEqual(campo.upload_to, upload_to)
    self.assertEqual(campo.height_field, height_field)
    self.assertEqual(campo.width_field, width_field)
    self.assertEqual(campo.max_length, max_length)

    # Pillow é obrigatorio para usar este tipo de field
    # SEE: docs.djangoproject.com/en/dev/ref/models/fields/#imagefield
    self.assertTrue(__import__('PIL'))


def field_integerfield(self, campo):
    pass


def field_ipaddressfield(self, campo):
    pass


def field_genericipaddressfield(
        self, campo, protocol='both', unpack_ipv4=False):
    self.assertEqual(campo.protocol, protocol)
    self.assertEqual(campo.unpack_ipv4, unpack_ipv4)


def field_nullbooleanfield(self, campo):
    pass


def field_positiveintegerfield(self, campo):
    pass


def field_positivesmallintegerfield(self, campo):
    pass


def field_slugfield(self, campo, max_length=50):
    self.assertEqual(campo.max_length, max_length)
    self.assertTrue(campo.db_index)

    return ['db_index']


def field_smallintegerfield(self, campo):
    pass


def field_textfield(self, campo):
    pass


def field_timefield(self, campo, **kwargs):
    return field_datefield(self, campo, **kwargs)


def field_urlfield(self, campo, max_length=200):
    self.assertEqual(campo.max_length, max_length)


def field_foreignkey(self, campo, model):
    self.assertEqual(campo.related.parent_model, model)
    self.assertTrue(campo.db_index)

    return ['db_index']


def field_manytomanyfield(self, campo, model):
    self.assertEqual(campo.related.parent_model, model)


def field_onetoonefield(self, campo, model):
    self.assertEqual(campo.related.parent_model, model)
