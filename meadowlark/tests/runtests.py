import os
import sys

from django.conf import settings

INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'basitapi',
	'django_nose',
	'meadowlark'
]

if not settings.configured:
	settings.configure(
		DATABASES={
			'default': {
				'ENGINE': 'django.db.backends.sqlite3',
				'NAME': ':memory:'
			}
		},
		INSTALLED_APPS=INSTALLED_APPS,
		ROOT_URLCONF='meadowlark.urls'
	)

from django_nose import NoseTestSuiteRunner

def runtests(*test_args):
	failures = NoseTestSuiteRunner(verbosity=2, interactive=True).run_tests(test_args)
	sys.exit(failures)

if __name__ == '__main__':
	runtests(*sys.argv[1:])