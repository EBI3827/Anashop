
import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
GOOGLE_RECAPTCHA_SECRET_KEY=config('GOOGLE_RECAPTCHA_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
        '127.0.0.1:8001',
        '*',
    ]


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'rest_framework',
    'captcha',
    'cities_light',
    'star_ratings',


    'product',
    'cart',
    'api',
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

ROOT_URLCONF = 'tpshop.urls'

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
                'product.context_processors.nav',
                # 'product.context_processors.get',


            ],
        },
    },
]

WSGI_APPLICATION = 'tpshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en','English'),
    ('fa', 'persian')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# allauth settings

AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

)

ACCOUNT_AUTHENTICATION_METHOD= ('username')

ACCOUNT_FORMS = {
'login': 'product.forms.CustomLoginForm',
'signup':'product.forms.CustomSignupForm',
'reset_password':'product.forms.CustomResetPasswordForm',

}
ACCOUNT_EMAIL_REQUIRED=True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

LOGIN_REDIRECT_URL='/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", "media_root")

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# cities-light settings

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['fa', 'en','abbr']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['IR']
CITIES_LIGHT_INCLUDE_CITY_TYPES = [
    'PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC',
    'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',
]

STAR_RATINGS_STAR_HEIGHT=STAR_RATINGS_STAR_WIDTH=14

