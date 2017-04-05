# Django with Mongo local setup

### About

A Django project template for Mongo Engine. Following is the setup instruction for local setup.

### Version 0.1

### Tech Stack

Following is the tech stack being used for main project:

* [Django 1.8] - The core Web Framework
* [Django Rest Framework 3.3.3] - For creating REST APIs
* [Any SQL Database] - As datastore
* [MongoDB 3.0] - As datastore
* [MongoEngine 0.10] - To let Django talk to MongoDB
* [Celery 3.1.23] - A task queue used for async processes and task scheduling
* [Redis 2.8.4] - As message broker, a result backend for Celery and for caching
* [Elastic Search] with [Haystack] for indexing data

### Project Setup
* Update ubuntu
```sh
sudo apt-get update
```

* Install python-pip
```sh
sudo apt-get install python-pip python-dev git
sudo apt-get install build-essential libssl-dev libffi-dev
```

* Install virtualenv and virtualenvwrapper:
```sh
sudo pip install virtualenv virtualenvwrapper
sudo pip install --upgrade pip
```

* Create a backup of the .bashrc file
```sh
cp ~/.bashrc ~/.bashrc-org
```

* Create a directory to store all the virtual environments
```sh
mkdir ~/.virtualenvs
```

* Set WORKON_HOME to virtual environments directory
```sh
export WORKON_HOME=~/.virtualenvs
```

* Open bashrc file
```sh
sudo nano ~/.bashrc
```

* Add the following line at the end of bashrc file:
```
. /usr/local/bin/virtualenvwrapper.sh
```

* Re-source terminal using the following command
```sh
source ~/.bashrc
```

* Create new virtual environment
```sh
mkvirtualenv project_mongo
```

* Activate the virtual environment
```sh
workon project_mongo
```


##### Fetching and Prepping the Project
* Create a parent folder called sites
```sh
mkdir sites && cd sites
```

* Clone the project
```sh
git clone https://github.com/eshandas/django_project_template_mongo.git
```

* Rename project directory for consistency and cd
```sh
mv django_project_template_mongo/ project_mongo && cd project_mongo
```

> NOTE: Install the following dependencies before installing Pillow:

```sh
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev
```

* Create a virtual env
```sh
mkvirtualenv project_mongo
```

* Point the local settings file in the virtualenv postactivate hook
```sh
deactivate
sudo nano ~/.virtualenvs/project_mongo/bin/postactivate
```

* Add the following line
```
...
export DJANGO_SETTINGS_MODULE=main.settings.local
```

* Remove the pointer once the env is deactivated
```sh
sudo nano ~/.virtualenvs/project_mongo/bin/postdeactivate
```

* Add the following line
```
...
unset DJANGO_SETTINGS_MODULE
```

* Reactivate the virtual env
```sh
deactivate project_mongo
workon project_mongo
```

* Install all the requirements
```sh
pip install -r requirements/local.txt
```

* Run migrations
```sh
python manage.py migrate
```

* Test by running
```sh
python manage.py runserver
```

##### Setting up Haystack and Elastic Search
Not required for now. Check _docs in case needed.

##### Setting up Celery
Not required for now. Check _docs in case needed.

##### Setting up Gunicorn
Not required for now. Check _docs in case needed.

##### Setting up Nginx
Not required for now. Check _docs in case needed.

##### Setup Supervisord
Not required for now. Check _docs in case needed.