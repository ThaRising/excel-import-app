import socket
from contextlib import closing

from .production import *  # noqa
from .keys import *  # noqa

DEBUG = True

ADMIN_EMAIL = 'root@root.com'
ADMIN_PASSWORD = 'root'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DJANGO_DB_NAME', 'default'),
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': os.getenv('DJANGO_DB_HOST', 'localhost'),
        'PORT': '5432',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Activate CORS
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # Let all CSRF checks pass that pass CORS
    'corsheaders.middleware.CorsPostCsrfMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_REPLACE_HTTPS_REFERER = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = [
    "127.0.0.1"
]
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
