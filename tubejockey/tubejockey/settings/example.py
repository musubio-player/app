from .base import *

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

SECRET_KEY = 'lsldkdkfj**fjsl%dkkk2nalsdlfkcj*0o2lk2lPPdks.hvhwu6s6JDJj22)Idjj2jhs'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}