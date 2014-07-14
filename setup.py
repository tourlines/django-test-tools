from distutils.core import setup
import test_tools


setup(
    name=test_tools.__title__,
    author=test_tools.__author__,
    version=test_tools.__version__,
    packages=['test_tools'],
    description='',
    author_email='romulo.santos@outlook.com',
    url='https://github.com/dullaran/django-test-tools',
    download_url='https://github.com/dullaran/django-test-tools/archive/master.zip',
    keywords='',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
