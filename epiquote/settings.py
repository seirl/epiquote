import configparser
import dj_database_url
import email.utils
import os
from django.contrib.messages import constants as messages
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
if config_path := os.getenv('EPIQUOTE_SETTINGS_PATH'):
    config.read(config_path)
if creds_path := os.getenv('EPIQUOTE_CREDS_PATH'):
    config.read(creds_path)

DEBUG = not config.getboolean('epiquote', 'prod', fallback=False)

if DEBUG:
    SECRET_KEY = config.get(
        'epiquote', 'secret_key', raw=True, fallback='CHANGE_ME'
    )
else:
    SECRET_KEY = config.get('epiquote', 'secret_key', raw=True)

ALLOWED_HOSTS = [
    h.strip()
    for h in config.get(
        'epiquote', 'allowed_hosts', fallback='127.0.0.1,::1,localhost'
    ).split(',')
]

DATABASES = {
    'default': dj_database_url.config(
        default=config.get(
            'epiquote',
            'database_url',
            fallback='sqlite:///epiquote.db',
        )
    ),
}

if config.getboolean('epiquote', 'show_emails_on_console', fallback=False):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = [
    email.utils.parseaddr(h.strip())
    for h in config.get('epiquote', 'admins', fallback='').split(',')
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

USE_X_FORWARDED_HOST = config.getboolean(
    'epiquote', 'use_x_forwarded_host', fallback=False
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
STATIC_ROOT = config.get('epiquote', 'static_root', fallback='')

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
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    'bootstrapform',
    # Epiquote
    'quotes',
)

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
AUTH_PROFILE_MODULE = 'quotes.UserProfile'

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
ENABLE_EPITA_CONNECT = config.getboolean(
    'epita_connect', 'enable', fallback=False
)
SOCIAL_AUTH_EPITA_SCOPE = ['email', 'epita']
SOCIAL_AUTH_EPITA_EXTRA_DATA = ['promo']
SOCIAL_AUTH_EPITA_KEY = config.get('epita_connect', 'auth_key', fallback=None)
SOCIAL_AUTH_EPITA_SECRET = config.get(
    'epita_connect', 'auth_secret', fallback=None
)
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
