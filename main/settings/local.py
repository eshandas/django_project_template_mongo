from main.settings.base import *

from mongoengine import connect
connect('connection_name', username='admin', password='******')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']


INSTALLED_APPS += (
    'debug_toolbar',
    'debug_panel',
    'django_extensions',
)


MIDDLEWARE_CLASSES += (
    'debug_panel.middleware.DebugPanelMiddleware',
)


# Haystack connection
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# AWS Settings
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


# Email server settings
# ABSOLUTELY REMOVE THE DUMMY EMAIL SERVER IN PRODUCTION!!!
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'email-smtp.xx-xxxx-x.amazonaws.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = AWS_ACCESS_KEY_ID
# EMAIL_HOST_PASSWORD = AWS_SECRET_ACCESS_KEY
