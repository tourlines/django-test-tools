# coding: utf-8
from django.test import TestCase
from ..utils import Option


class AdminTestCase(TestCase):

    @property
    def admin(self):
        raise NotImplementedError(
            'Crie uma variável contendo o model que esta sendo testado')

    @property
    def model(self):
        raise NotImplementedError(
            'Crie uma variável contendo o model que esta sendo testado')

    @property
    def admin_fields(self):
        NotImplementedError(
            'Diga-nós quais são os atributos presentes no admin')

    def _validar_admin(self, **kwargs):
        from django.forms.models import ModelForm
        from django.core.paginator import Paginator

        OPTIONS = [
            Option('actions', []),
            Option('actions_on_top', True),
            Option('actions_on_bottom', False),
            Option('actions_selection_counter', True),
            Option('date_hierarchy', None),
            Option('exclude', None),
            Option('fields', None),
            Option('fieldsets', None),
            Option('filter_horizontal', ()),
            Option('filter_vertical', ()),
            Option('form', ModelForm),
            Option('formfield_overrides', {}),
            Option('inlines', []),
            Option('list_display', ()),
            Option('list_display_links', ()),
            Option('list_editable', ()),
            Option('list_filter', ()),
            Option('list_max_show_all', 200),
            Option('list_per_page', 100),
            Option('list_select_related', False),
            Option('ordering', None),
            Option('paginator', Paginator),
            Option('prepopulated_fields', {}),
            Option('preserve_filters', None, (1, 6, 0)),
            Option('radio_fields', {}),
            Option('raw_id_fields', ()),
            Option('readonly_fields', ()),
            Option('save_as', False),
            Option('save_on_top', False),
            Option('search_fields', ()),
            Option('view_on_site', None, (1, 7, 0)),
            Option('add_form_template', None),
            Option('change_form_template', None),
            Option('change_list_template', None),
            Option('delete_confirmation_template', None),
            Option('delete_selected_confirmation_template', None),
            Option('object_history_template', None),
        ]

        for option in OPTIONS:
            if option.e_compativel_django():
                valor = kwargs.get(option.nome) or option.default
                admin_option = getattr(self.admin, option.nome)
                self.assertEqual(
                    admin_option,
                    valor,
                    'Opção %s deveria ser %s, mas é %s' % (
                        option.nome, valor, admin_option)
                )

    def validar_admin(self):
        from django.contrib import admin

        self._validar_admin(**self.admin_fields)
        self.assertTrue(
            isinstance(admin.site._registry[self.model], self.admin))
