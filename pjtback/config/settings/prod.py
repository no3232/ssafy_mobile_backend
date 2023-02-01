from .base import *

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_mobile',
        'USER': 'root',
        'PASSWORD': 'sangjun1324',
        'HOST': 'db',
        'PORT': '3306'
    }
}