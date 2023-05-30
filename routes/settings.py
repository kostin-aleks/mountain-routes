"""
Django settings for routes project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, "data")
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'routes.mountains',
    'routes.api',
    'django_tables2',
    'django_filters',
    'django_registration',
    # 'drf_spectacular',
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_swagger',
    'routes.user',
    'routes.geoname',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'routes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'routes/templates/'),
                 os.path.join(BASE_DIR, 'routes/templates/admin/'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'routes.context.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'routes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASE_NAME = env('DATABASE_NAME')
DATABASE_USER = env('DATABASE_USER')
DATABASE_PASSWORD = env('DATABASE_PASSWORD')
DATABASE_HOST = env('DATABASE_HOST')
DATABASE_PORT = env('DATABASE_PORT')

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': BASE_DIR / 'db.sqlite3',
# }
# }

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.postgresql_psycopg2',
# 'NAME': DATABASE_NAME,
# 'USER': DATABASE_USER,
# 'HOST': DATABASE_HOST,
# 'PASSWORD': DATABASE_PASSWORD,
# 'PORT': DATABASE_PORT,
# 'ATOMIC_REQUESTS': True,
# 'CONN_MAX_AGE': POSTGRES_CONN_MAX_AGE,
# }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "PORT": DATABASE_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGE_CODES = ['ru', 'en']

if 'ru' in LANGUAGE_CODES:
    LANGUAGE_CODE = 'ru'
else:
    LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Русский'),
)

DEFINED_LANGUAGES = {
    'en': {'title': 'English', 'short': 'ENG'},
    'ru': {'title': 'Русский', 'short': 'РУС'},
}
LANGUAGES = [(k, DEFINED_LANGUAGES[k]['title']) for k in DEFINED_LANGUAGES if k in LANGUAGE_CODES]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale")
]

LANGUAGE_COOKIE_NAME = "gpsfun_lang"

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "d.m.Y"
TIME_FORMAT = "H:i"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "routes/static/"),
)
STATIC_TEST_DATA = os.path.join(STATICFILES_DIRS[0], 'test_images/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Registration

ACCOUNT_ACTIVATION_DAYS = 2

ADMINS = ()

SAFE_EMAILS = env.list('SAFE_EMAILS')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

COMMENTS_PER_PAGE = env('COMMENTS_PER_PAGE')
COMMENT_IMG_WIDTH = 320
COMMENT_IMG_HEIGHT = 240
COMMENT_TXT_SIZE_KB = 100

try:
    from .custom_settings import *

except ImportError:
    pass
