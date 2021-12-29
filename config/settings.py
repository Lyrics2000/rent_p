
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r6=r%x@ga9$si=_d9=1!i!yg@h5kh%2v3knfbna##y9d_njmo3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.herokuapp.com','127.0.0.1','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django', # add this
    'django.contrib.gis',
    'djgeojson',
    'homepage',
    'account',
    'leaflet',
    'rest_framework',
     'rest_framework_gis',
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

ROOT_URLCONF = 'config.urls'
AUTH_USER_MODEL = 'account.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR/'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# add this
AUTHENTICATION_BACKENDS = [
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_FACEBOOK_KEY = "511593623354651"        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "4edaa433cf9a77e4e8f147eea0cfd710"
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'rentb',
#         'USER': 'rudi',
#         'PASSWORD': 'Lyrics254',
#         'HOST': '127.0.0.1',
#         'POST': '',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dfdhevlih6k24d',
        'USER': 'zrjgbpazsocwgv',
        'PASSWORD': '8a156a110b452e1e335362bb04ecf0f877f8ef05c5ebdffff5cc19d226df52ca',
        'HOST': 'ec2-54-204-99-176.compute-1.amazonaws.com',
        'POST': 5432,
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LEAFLET_WIDGET_ATTRS = {
   'map_height': '500px',
   'map_width': '100%',
   'display_raw': 'true',
   'map_srid': 4326,
}

LEAFLET_CONFIG = {
       'DEFAULT_CENTER': (0.023, 36.87),
       'DEFAULT_ZOOM':5,
        'MAX_ZOOM': 20,
        'MIN_ZOOM':1,
        'SCALE': 'both',
        'ATTRIBUTION_PREFIX': 'Powered by Rentobay Ltd',
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# development
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_file'),
]

STATIC_ROOT = os.path.join('static_cdn')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('media_cdn')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'thomasambetsa@gmail.com'
EMAIL_HOST_PASSWORD = 'wojjleviqxakkazs'
EMAIL_PORT = 587
