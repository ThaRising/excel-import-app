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
        'NAME': 'default',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
    sock.settimeout(5)
    current_port = int(DATABASES['default']['PORT'])
    if sock.connect_ex(('localhost', current_port)) != 0:
        DATABASES['default']['HOST'] = 'database'

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
