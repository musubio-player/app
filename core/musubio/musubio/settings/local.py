from .base import *

SECRET_KEY = 'idi*7dh2lol++_-d02llsbnndmmMMCCsk2jd9c87vhJJ@&&e6^^28sk'
DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'musubio',
        'USER': 'musubio',
        'PASSWORD': 'musubio',
        'HOST': '',
        'PORT': '',
    },
    'mongodb': {
        'NAME': 'musubio',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '27017',
    }
}