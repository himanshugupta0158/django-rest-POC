"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sejic5w$a(bki^=dc(=mizw%0s!&yvy0pa$c7=1rviavz&r^pb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django support libraries like for APIs and designing templates
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap4',
    
    # 3rd party
    'django_filters',
    "debug_toolbar",

    # Django Apps
    'api',
    'institute',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'

# The directory where 'collectstatic' will collect static files.
STATIC_ROOT = 'staticfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# For REST FRAMEWORK GLOBAL Pagination defining
# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 25
# }


# For Filtering
# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS' : [
#         'django_filters.rest_framework.DjangoFilterBackend'
#     ]
# }

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # Use 'bootstrap4' for Bootstrap 4, or 'bootstrap3' for Bootstrap 3


CRISPY_CLASS_CONVERTERS = {
    'textinput': 'form-control',
    'fileinput': 'form-control-file',
    'clearablefileinput': 'form-control-file',
}

CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni-form', 'bootstrap3', 'bootstrap4')
CRISPY_USE_LEGACY_CLASSES = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"


# Logout Redirect page
LOGOUT_REDIRECT_URL = 'login'


# password Reset settings and for sending mail on gmail
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'your_email_host'  # For example, 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'your_email@example.com'
# EMAIL_HOST_PASSWORD = 'your_email_password'

# Django debug toolbar

###### Important to show ############
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

