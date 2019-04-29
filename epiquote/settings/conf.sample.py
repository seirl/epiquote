from .common import *  # noqa


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

# Uncomment to enable EPITA social auth:
#
# ENABLE_EPITA_CONNECT = True
# SOCIAL_AUTH_EPITA_KEY = "CHANGEME"
# SOCIAL_AUTH_EPITA_SECRET = "CHANGEME"
# AUTHENTICATION_BACKENDS += ('epita_connect.backend.EpitaOpenIdConnect',)
# if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
#     SOCIAL_AUTH_POSTGRES_JSONFIELD = True

# Uncomment to enable showing the emails on the console
#
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
