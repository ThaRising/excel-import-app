import os

import dj_database_url
import django
from BauerDude.docs.settings import *  # noqa
from datetime import timedelta
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
TESTING = 'test' in sys.argv  # detect if we are running tests
SECRET_KEY = os.getenv('SECRET_KEY')

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

SILKY_META = True
SILKY_PYTHON_PROFILER = True
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
LOGIN_URL = "/djprofile/login/"


INSTALLED_APPS = [
    'drizm_django_commons',  # manage.py overrides
    'BauerDude.application.CustomAdmin',  # default admin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'silk',

    # Default apps
    'BauerDude.apps.users',
    'BauerDude.apps.tokens',

    # User defined apps
    'BauerDude.apps.products',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



""" ORM Config """
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}



""" Auth / Security Config """
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER':
        'BauerDude.lib.errors.handler.global_default_exception_handler'  # noqa
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

ALLOWED_HOSTS = [
    # Domain of the site you're planning to host on here
    '.herokuapp.com'
]

AUTH_USER_MODEL = 'users.User'



""" CORS Configuration """
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]
CORS_EXPOSE_HEADERS = [
    "Content-Disposition"
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    # Domain of the site you're planning to host on here
    r"^https://\w+\.herokuapp\.com$",
]
# This applies only to cookies, the integrated system
# is using Header based Token-Auth
CORS_ALLOW_CREDENTIALS = False
# Anything longer than 10 minutes is pointless for REST
CROS_PREFLIGHT_MAX_AGE = 600



""" File Handling Config """
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "media"),
]
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)



""" Internationlization Config """
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'



""" You probably wont need to touch these """
ROOT_URLCONF = 'BauerDude.urls'
WSGI_APPLICATION = 'BauerDude.wsgi.application'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Without the changes in FORM_RENDERER and TEMPLATE["DIRS"]
# global template directories would not work properly
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(django.__path__[0] + '/forms/templates'),
        ],
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
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
