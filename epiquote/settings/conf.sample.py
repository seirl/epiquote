from .common import *  # noqa
import os


DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# You can generate a key using the following command:
# openssl rand -base64 64 | sed "s/[/10lO#+=]//g" | tr -d "\n"; echo
SECRET_KEY = 'CHANGEME'

ALLOWED_HOSTS = ['127.0.0.1', '::1', 'localhost']

SITE_HOST = "localhost:8000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'epiquote.db',
    }
}

BASE_DIR = os.getcwd()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'quotes/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
