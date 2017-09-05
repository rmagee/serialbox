# Installation
Installing and running *SerialBox* requires a working knowledge of
[Django](http://www.thedjangoproject.com).  Prior to installing SerailBox,
you should understand how to start a Django project/app and configure it for
database access.  

## Create a new Django Project
```
mkdir ~/Downloads/sbdemo
python django-admin.py startproject sbdemo ~/Downloads/sbdemo
cd ~/Downloads/dbdemo
```


## Modify Your settings.py Module
Add django rest framework and serialbox to your installed apps by putting
`serialbox.pools` in your settigns file's `INSTALLED_APPS` as in the example
below:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'serialbox.pools',
]
```

## Add Serialbox URLS to your urls.py Module

```
from django.conf.urls import url, include
from serialbox.api import urls

urlpatterns = [
    url(r'^serialbox/', include(urls)),
]
```

## Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```

## Execute the Unit Tests

### Using Your Settings File
```
python manage.py test serialbox
```

### Using the Test Settings File
The SerialBox unit tests can be run independently using a sqlite database
by executing the unit tests as in the example below:
```
python manage.py test serialbox --settings=serialbox.pools.tests.settings
```

Your SerialBox installation should be complete at this point.  You can
run the Django development server to test or hook into your favorite
web server.  For more on running and configuring Django see the
[The Django Project web site.](http://www.thedjangoproject.com)
