"""
Django settings for wumpus project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import decouple
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = decouple.config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = decouple.config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = decouple.config('ALLOWED_HOSTS', cast=decouple.Csv())

# Application definition

INSTALLED_APPS = [
    'gallery.apps.GalleryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'widget_tweaks',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
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

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


ROOT_URLCONF = 'wumpus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'wumpus.wsgi.application'

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                },
            },
        'loggers': {
            'gallery': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
                },
            },
        }

INTERNAL_IPS = ['127.0.0.1'] # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': decouple.config('DB_NAME'),
            'USER': decouple.config('DB_USER'),
            'PASSWORD': decouple.config('DB_PASSWORD'),
            'HOST': decouple.config('DB_HOST'),
            'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = decouple.config('STATIC_ROOT')


# File uploads
FILE_UPLOAD_PERMISSIONS = 0o644

# Force all uploads to be written to disk. We need this for exiftool.
# (XXX technically we could send the small in-memory uploads to exiftool's
# stdin -- investigate!)
FILE_UPLOAD_MAX_MEMORY_SIZE = 0

#CURRENT_DIR = os.path.dirname(__file__)
#MEDIA_ROOT = os.path.join(CURRENT_DIR, 'media')
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = decouple.config('MEDIA_ROOT')
MEDIA_URL = '/media/'

IMAGEKIT_CACHEFILE_DIR = 'thumbnails' # Put thumbnails in the same directory as originals
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'gallery.namers.source_name_as_path'
IMAGEKIT_DEFAULT_FILE_STORAGE = 'gallery.storage.ThumbnailStorage'

# The first size will be the default preview size
GALLERY_THUMBNAIL_SIZES = [240, 320, 500, 640, 800, 1024, 1600, 2048]
# When viewing a photo, we actually display a thumbnail of the following size, not the original
PHOTO_DETAIL_THUMBNAIL_SIZE = 1600
# Settings for Justified Gallery
JG_ROW_HEIGHT = 320
JG_MARGINS = 5

EXIFTOOL = decouple.config('EXIFTOOL', default='exiftool')
