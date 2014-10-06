# coding: utf-8


def option_widget(self, atributo, nome, widget=None, **kwargs):
    from django.forms import fields, widgets

    # Quando o field for um built-in do Django podemos deixar que o usuário
    # passe apenas uma string, e importamos o widget do django
    if isinstance(widget, basestring):
        widget = getattr(widgets, widget)

    # Quando o usuário não passar o widget a ser usado, precisamos validar o
    # seu valor default, contudo cada field do django possui um widget
    # particular e por isto precisamos detectar qual é o widget que esperamos
    # que o field tenha
    if not widget:
        relacoes_field_widgets = [
            (fields.BooleanField, widgets.CheckboxInput),
            (fields.CharField, widgets.TextInput),
            (fields.ChoiceField, widgets.Select),
            (fields.TypedChoiceField, widgets.Select),
            (fields.DateField, widgets.DateInput),
            (fields.DateTimeField, widgets.DateTimeInput),
            (fields.DecimalField, widgets.TextInput),
            (fields.EmailField, widgets.TextInput),
            (fields.FileField, widgets.ClearableFileInput),
            (fields.FilePathField, widgets.Select),
            (fields.FloatField, widgets.TextInput),
            (fields.ImageField, widgets.ClearableFileInput),
            (fields.IntegerField, widgets.NumberInput),
            (fields.IPAddressField, widgets.TextInput),
            (fields.GenericIPAddressField, widgets.TextInput),
            (fields.MultipleChoiceField, widgets.SelectMultiple),
            (fields.TypedMultipleChoiceField, widgets.SelectMultiple),
            (fields.NullBooleanField, widgets.NullBooleanSelect),
            (fields.RegexField, widgets.TextInput),
            (fields.SlugField, widgets.TextInput),
            (fields.TimeField, widgets.TextInput),
            (fields.URLField, widgets.TextInput),
        ]

        for relacao in relacoes_field_widgets:
            if isinstance(atributo, relacao[0]):
                widget = relacao[1]
                break

    self.assertIsInstance(atributo.widget, widget)
