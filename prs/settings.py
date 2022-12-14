"""
Django settings for prs project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import json, os
from appconfig import app, host, sped, ldap
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w3xz7@!)cst4&i^h5c&e&chul@whi428*8i*u+mein1!ch*g+&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = host["names"]

CHANGELOG = json.loads(open("changelog.json", "r", encoding="utf-8").read())
# Application definition

INSTALLED_APPS = [
    'sped',
    'requisicoes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'prs.urls'

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

WSGI_APPLICATION = 'prs.wsgi.application'

if sped.get('host'):
    POST_HOST = sped.get('host')
    POST_USER = sped.get('post_user',os.environ['POST_USER'])
    POST_PASSWORD = sped.get('post_pass',os.environ['POST_PASSWORD'])
    POST_AUTHDB = sped.get('database',os.environ['POST_AUTHDB'])
    BASE_DN    = sped.get('base_dn', ldap.get('base_dn', 'dc=eb,dc=mil,dc=br') )
    LDAP_HOST = sped.get('host', ldap.get('host', 'ldap') )
else:
    POST_HOST = os.environ['POST_HOST']
    POST_USER = os.environ['POST_USER']
    POST_PASSWORD = os.environ['POST_PASSWORD']
    POST_AUTHDB = os.environ['POST_AUTHDB']
    BASE_DN    = ldap.get('base_dn', 'dc=eb,dc=mil,dc=br')
    LDAP_HOST = ldap.get('host', 'ldap')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POST_APPDB'],
        'USER': os.environ['POST_USER'],
        'PASSWORD': os.environ['POST_PASSWORD'],
        'HOST': os.environ['POST_HOST'],
        'PORT': '5432'
    },
    'dbpgsped': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POST_AUTHDB,
        'USER': POST_USER,
        'PASSWORD': POST_PASSWORD,
        'HOST': POST_HOST,
        'PORT': '5432'
    }
}
DATABASE_ROUTERS = ['router.sped.dbpgspedRouter']

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OMENDERECO = app.get('orgendereco')
ALLOWED = app.get('allowed_ext')
MAXSIZE = int(app.get('maxtotalfsize'))

AUTH_LDAP_SERVER_URI = "ldap://%s"%(LDAP_HOST)
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_DN_TEMPLATE = "cn=%(user)s,"+BASE_DN

AUTHENTICATION_BACKENDS = ['django_auth_ldap.backend.LDAPBackend',
                           'django.contrib.auth.backends.ModelBackend']

MEDIA_ROOT = BASE_DIR / 'uploads/'
MEDIA_URL = '/uploads/'

