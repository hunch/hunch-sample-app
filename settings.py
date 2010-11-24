# Django settings for Hunch applications

from djangoappengine.settings_base import *

import os

############
# Edit me! #
############

# your SECRET_KEY should be a unique 50 character string.
SECRET_KEY = '##################################################'

# you can use the following code to generate it:

# import string
# from random import choice
# print ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])

DEBUG = True

##################
# Don't touch me #
##################
INSTALLED_APPS = (
    'djangoappengine',
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

