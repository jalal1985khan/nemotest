"""
Django settings for nsnemo project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w*-*9&+69^x(unfhrc9*^e2)q7u+_0qj#qhx#q$jh0+l7!(&%b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://django.ivistasolutions.biz']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic', #Make sure to add this 
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nemo',
    'widget_tweaks',
   
  
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #make sure to add this line
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nsnemo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,"templates", "staticfiles"],
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

WSGI_APPLICATION = 'nsnemo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ= True
TIME_ZONE = 'Asia/Calcutta'

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/staticfiles/'
MEDIA_URL ='/media/'
#STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),

#STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#    os.path.join(BASE_DIR, 'static')
#]

#BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'static')
#STATIC_ROOT = BASE_DIR/ "static/"
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# STATICFILES_DIRS = [
#     BASE_DIR/ "staticfiles",
    
# ]
MEDIA_ROOT = BASE_DIR/"staticfiles/images"
STATIC_ROOT = BASE_DIR/ "staticfiles/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False if DEBUG else True,
    "formatters": {
        "verbose": {
            "format": '%(levelname)s %(asctime)s %(module)s %(message)s',
           # "class":"pythonjsonlogger.jsonlogger.Jsonformatter"
        },
        "simple": {
            "format": '%(levelname)s %(asctime)s %(module)s %(message)s',
           # "class":"pythonjsonlogger.jsonlogger.Jsonformatter"
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": 'DEBUG' if DEBUG else 'INFO',
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
"info":{
    'level':'INFO',
    'class':'logging.handlers.RotatingFileHandler',
    'filename':os.path.join(BASE_DIR, 'log/info.log'),
    'maxBytes':300 * 1024 * 1024, #300M size
    'backupCount':10,
    'formatter':'verbose',
    'encoding':'utf-8'
},
'logger':{
    "django":{
        "handler":["info", "console"],
        "propagate":True,
        "level": "INFO"
    }
}

}