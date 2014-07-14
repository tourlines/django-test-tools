#!/bin/bash


export PYTHONPATH=$(dirname $0)
django-admin.py test --settings=test.settings $1
