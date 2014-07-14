# coding: utf-8
import os
import sys
from decouple import config
from dj_database_url import parse as db_url
from unipath import Path


BASE_DIR = Path(__file__).parent
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY', default='XXXXXXXXX')

AMBIENTE_TESTES_GERAL = True

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url
    ),
}

PROJECT_APPS = (
    'test.core',
)

INSTALLED_APPS = (
    # Bibliotecas padrões do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Bibliotecas Externas
    'south',
    'django_jenkins',

    # Aplicações para testes
    'django_nose',
) + PROJECT_APPS

TESTING = 'test' in sys.argv or 'jenkins' in sys.argv

# NoseTests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nologcapture',
    '--nocapture',
    '--verbosity=1',
]

# Estes argumentos exibem muitas informações na sua saída, estas informações
# são usadas pelo jenkins para relatorio e portanto apenas devem ser exibidas
# quando estiver no ambiente do jenkins.
if os.environ.get('JENKINS'):
    NOSE_ARGS += [
        '--with-xcoverage',
        '--cover-erase',
        '--with-xunit',
        '--xunit-file=%s' % (os.path.join(ROOT_PATH, 'reports/junit.xml')),
        '--xcoverage-file=%s' % (
            os.path.join(ROOT_PATH, 'reports/coverage.xml')),
    ]

# O argumento where do nose deve SEMPRE estar no final das opções. Ele diz ao
# nose em qual workspace o mesmo esta trabalhando possibilitando a inserção de
# varios workspaces e devido a esta carateristica quaisquer nomes que estejam
# após a esta opção é tratada como uma pasta onde ele vai buscar os testes
NOSE_ARGS.append('--where=%s' % (ROOT_PATH))

# Django-Jenkins
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_flake8',
    #'django_jenkins.tasks.run_sloccount',
)
JENKINS_TEST_RUNNER = 'django_jenkins.runner.CITestSuiteRunner'
