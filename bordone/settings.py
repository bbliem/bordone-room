import decouple
import os

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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
    'django.contrib.sites',
    'django.contrib.flatpages',
    'imagekit',
    'widget_tweaks',
]

# We only serve one site, but we need the sites framework for flatpages.
# https://docs.djangoproject.com/en/2.1/ref/contrib/flatpages/
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'bordone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'bordone.wsgi.application'

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                },
            'djangologfile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR / 'django.log',
                'maxBytes': 1024*1024*15, # 15MB
                'backupCount': 10,
                },
            'applogfile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR / 'gallery.log',
                'maxBytes': 1024*1024*15, # 15MB
                'backupCount': 10,
                },
            },
        'loggers': {
            'django': {
                'handlers': ['console', 'djangologfile'],
                'level': decouple.config('DJANGO_LOG_LEVEL', default='INFO'),
                },
            'gallery': {
                'handlers': ['console', 'applogfile'],
                'level': decouple.config('GALLERY_LOG_LEVEL', default='INFO'),
                },
            },
        }

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': decouple.config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': decouple.config('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        'USER': decouple.config('DB_USER', default=None),
        'PASSWORD': decouple.config('DB_PASSWORD', default=None),
        'HOST': decouple.config('DB_HOST', default=None),
        'PORT': decouple.config('DB_PORT', default=None),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = decouple.config('TIME_ZONE', default='UTC')
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


# Testing
TEST_RUNNER = 'gallery.runner.CustomDiscoverRunner'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = decouple.config('STATIC_URL', default='/static/')
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
MEDIA_URL = decouple.config('MEDIA_URL', default='/media/')

# If serving from a subdirectory, you may want to set FORCE_SCRIPT_NAME
FORCE_SCRIPT_NAME = decouple.config('FORCE_SCRIPT_NAME', default=None)

# If Django is behind a reverse proxy, set USE_PROXY_HEADERS to true to make
# Django use the X-Forwarded-Proto and X-Forwarded-Host headers for generating
# URLs. (Make sure your reverse proxy sets these headers. See the README.)
if decouple.config('USE_PROXY_HEADERS', default=False, cast=bool):
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

IMAGEKIT_CACHEFILE_DIR = 'thumbnails' # Put thumbnails in this subdirectory of MEDIA_ROOT
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'gallery.namers.source_name_as_path'
IMAGEKIT_DEFAULT_FILE_STORAGE = 'gallery.storage.ThumbnailStorage'
# We take care of generating thumbnails ourselves when photos are uploaded and
# we do not need (or want to) generate them when access to a thumbnail is
# attempted.
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'

# The first size will be the default preview size
GALLERY_THUMBNAIL_SIZES = [240, 320, 500, 640, 800, 1024, 1600, 2048]
# When viewing a photo, we actually display a thumbnail of the following size, not the original
PHOTO_DETAIL_THUMBNAIL_SIZE = 1600
# Size of thumbnails used for previews on social media
SOCIAL_MEDIA_THUMBNAIL_SIZE = 640
# Settings for Justified Gallery
JG_ROW_HEIGHT = 320
JG_MARGINS = 5

EXIFTOOL = decouple.config('EXIFTOOL', default='exiftool')
