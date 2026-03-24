import dj_database_url
import email.utils
import os
import tomllib
from django.contrib.messages import constants as messages
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

config = {}

def load_config(path):
    try:
        with open(path, 'rb') as f:
            toml_data = tomllib.load(f)
            for section, options in toml_data.items():
                if section not in config:
                    config[section] = {}
                config[section].update(options)
    except FileNotFoundError:
        pass

if config_path := os.getenv('EPIQUOTE_SETTINGS_PATH'):
    load_config(config_path)
if creds_path := os.getenv('EPIQUOTE_CREDS_PATH'):
    load_config(creds_path)

epiquote_config = config.get('epiquote', {})

DEBUG = not epiquote_config.get('prod', False)

if DEBUG:
    SECRET_KEY = epiquote_config.get('secret_key', 'CHANGE_ME')
else:
    SECRET_KEY = epiquote_config.get('secret_key')

ALLOWED_HOSTS = [
    h.strip() if isinstance(h, str) else h
    for h in epiquote_config.get(
        'allowed_hosts', ['127.0.0.1', '::1', 'localhost']
    )
]

DATABASES = {
    'default': dj_database_url.config(
        default=epiquote_config.get(
            'database_url',
            'sqlite:///epiquote.db',
        )
    ),
}

if epiquote_config.get('show_emails_on_console', False):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = [
    email.utils.parseaddr(h.strip())
    for h in epiquote_config.get('admins', [])
]


MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

USE_X_FORWARDED_HOST = epiquote_config.get(
    'use_x_forwarded_host', False
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = epiquote_config.get('static_root', '')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'epiquote/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'epiquote.context_processors.inject_settings',
            ],
        },
    },
]

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'epiquote.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'epiquote.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Vendor
    'django_comments',
    'django_registration',
    'crispy_forms',
    'crispy_bootstrap5',
    # Epiquote
    'quotes',
)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console_debug_false': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console_debug_false'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

ACCOUNT_ACTIVATION_DAYS = 1
DEFAULT_FROM_EMAIL = 'Epiquote <noreply@epiquote.fr>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/accounts/login'
DATABASE_ENGINE = 'sqlite3'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Quotes pagination
QUOTES_MAX_PAGE = 50
QUOTES_MAX_PAGE_HOME = 5

# EPITA Connect
epita_connect_config = config.get('epita_connect', {})

ENABLE_EPITA_CONNECT = epita_connect_config.get('enable', False)
SOCIAL_AUTH_EPITA_SCOPE = ['email', 'epita']
SOCIAL_AUTH_EPITA_EXTRA_DATA = ['promo']
SOCIAL_AUTH_EPITA_KEY = epita_connect_config.get('auth_key')
SOCIAL_AUTH_EPITA_SECRET = epita_connect_config.get('auth_secret')

if ENABLE_EPITA_CONNECT:
    INSTALLED_APPS += ('social_django',)
    AUTHENTICATION_BACKENDS += ('epita_connect.backend.EpitaOpenIdConnect',)
    MIDDLEWARE += ('social_django.middleware.SocialAuthExceptionMiddleware',)
if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
    SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_auth_backend_epita.pipeline.deny_old_users",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_auth_backend_epita.pipeline.merge_old_users",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "social_auth_backend_epita.pipeline.update_email",
)
