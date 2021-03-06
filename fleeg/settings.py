import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('APP_SECRET_KEY',
                       '@kih_p6c%p4f5)wz5z4y=pn$t5e=$7!89g6bg(r8-*s#er((bw')

# SECURITY WARNING: don't run with debug or testing turned on in production!
TESTING = True if 'test' in sys.argv else False
DEBUG = True if 'runserver' in sys.argv or TESTING else False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'account',
    'link',
    'notification',
    'search',
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

ROOT_URLCONF = 'fleeg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'common/templates'),
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

WSGI_APPLICATION = 'fleeg.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
}

DATABASES = {
    'default': {
        'ENGINE': engines.get(os.getenv('DATABASE_ENGINE', 'sqlite')),
        'NAME': os.getenv('DATABASE_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LOGIN_URL = '/account/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'common/static'),
    os.path.join(BASE_DIR, 'media'),
]

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/avatar')


if TESTING:
    # ADD NOSE TO TEST AND COVERAGE APPS
    INSTALLED_APPS.append('django_nose')

    # Use nose to run all tests
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
