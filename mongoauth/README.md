# Mongoauth

A custom MongoDB based Django Authentication Layer for Django 1.8

## Usage
### Install Packages
* [Django Rest Framework 3.3.3]
* [MongoDB 3.0]
* [MongoEngine 0.10]

### Setup
Go to the **settings.py** file and make the following changes:

* Import and connect MongoEngine
```
from mongoengine import connect
connect('connection_name', username='admin', password='******')
```
* Unplug the default **'django.contrib.auth'** and plug our custom **'mongoauth'**
in **INSTALLED_APPS**. Also unplug the **'django.contrib.admin'** app as it serves
no purpose to us anymore
```
INSTALLED_APPS = (
    ...
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'mongoauth',
    ...
)
```
* Unplug the default middleware **'django.contrib.auth.middleware.AuthenticationMiddleware'** and plug our custom **'mongoauth.middleware.AuthenticationMiddleware'**
in **MIDDLEWARE_CLASSES**
```
MIDDLEWARE_CLASSES = (
    ...
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mongoauth.middleware.AuthenticationMiddleware',
    ...
)
```
> **NOTE:** The order of the middleware matters. So put it in the exact position.

* Add the custom authentication backend in **AUTHENTICATION_BACKENDS**
```
AUTHENTICATION_BACKENDS = (
    'mongoauth.backends.MongoAuthBackend',
)
```

* Change the session engine so that it does not use any SQL DB
```
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
```

* Change the default database to dummy (which basically turns off usage of SQL server)
```
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}
```



[Django Rest Framework 3.3.3]: http://www.django-rest-framework.org/#tutorial
[MongoDB 3.0]: https://docs.mongodb.org/v3.0/tutorial/install-mongodb-on-ubuntu/
[MongoEngine 0.10]: https://mongoengine-odm.readthedocs.org/tutorial.html