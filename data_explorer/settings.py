import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
from dotenv import load_dotenv
ENV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ENV_DIR, 'env', 'creds.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1ifa#n&(f#mig6^+!=*mo3^5x9qd%-^1b90fj$@g8j$^=ylg#u'
DEBUG = True

ALLOWED_HOSTS = ['localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
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

ROOT_URLCONF = 'data_explorer.urls'

WSGI_APPLICATION = 'data_explorer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'clickhouse_backend.backend',
        'NAME': os.getenv('CLICKHOUSE_DB', 'analytics'),
        'USER': os.getenv('CLICKHOUSE_USER', 'user'), 
        'PASSWORD': os.getenv('CLICKHOUSE_PASSWORD', 'clickhouse'), 
        'HOST': 'clickhouse', 
        'PORT': '9000', 
    }
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',  # You can specify a formatter for better readability
        },
        'console': {
            'level': 'INFO',  # Change this to 'DEBUG' if you want to see all debug messages
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # Specify a formatter for console output
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',  # Set the root level to DEBUG to catch all logging events
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',  # Keep DEBUG level for Django's logs
            'propagate': True,
        },
        # Example of a custom logger configuration (if you are using one in your app)
        'core': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # You can control levels per app
            'propagate': False,
        },
        'data_explorer': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # You can control levels per app
            'propagate': False,
        },
    },
}
