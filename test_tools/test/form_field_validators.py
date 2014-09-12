# coding: utf-8


def field_charfield(self, campo):
    pass


def field_datefield(self, campo):
    pass


def field_integerfield(self, campo, min_value, max_value):
    self.assertEqual(campo.min_value, min_value)
    self.assertEqual(campo.max_value, max_value)


def field_choicefield(self, campo, choices=()):
    self.assertItemsEqual(campo.choices, choices)


def field_booleanfield(self, campo):
    pass
