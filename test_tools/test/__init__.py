from .test_case import DjangoTestCase, UnittestTestCase
from .test_admin import AdminTestCase
from .test_form import FormTestCase
from .test_model import ModelTestCase

try:
    import cms
except ImportError:
    pass
else:
    from .test_model import CMSPluginModelTestCase
    from .test_cms_plugins import CMSPluginTestCase
