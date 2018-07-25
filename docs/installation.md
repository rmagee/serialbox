# Installation
Installing and running *SerialBox* requires a working knowledge of
[Django](http://www.thedjangoproject.com) and the 
[Django Rest Framework](http://django-rest-framework.org).  Prior to installing SerialBox,
you should probably understand how to start a Django project/app and configure it for
database access.  Nevertheless, instructions for getting everything up and 
running are below...


## Create a new Django Project
```
mkdir ~/sbdemo
python django-admin.py startproject sbdemo ~/sbdemo
cd ~/dbdemo
```

## Download and Install SerialBox
If you downloaded the SerialBox code from the repository and execute the following
in the root directory.
```
python setup.py install 
```

...otherwise, execute:

```
pip install serialbox
```

SerialBox will install Django and the Django Rest Framework as dependencies- along
with the `djangorestframework-xml` and `djangorestframework-csv` packages which are
necessary for XML and CSV support in the SerialBox API.


## Modify Your settings.py Module
Add django rest framework and serialbox to your installed apps by adding
`serialbox` and then `rest_framework` in your settings file's `INSTALLED_APPS` as in the example
below.  

### Optionally Use the .env File to set Environment Variables
If you wish to use environment variables to drive your database connections,
see the [Environment Variables](environment_variables.md) section.

SerialBox uses the [Django Rest Framwork](http://django-rest-framework.org),
if you wish to utilize the CSV, XML and Form functionality,
you can import the REST_FRAMEWORK settings as below or enable the available
features of the framework according to your needs.  JSON will be enabled
by default if you choose not to enable the additional renderers and parsers
defined in the REST_FRAMEWORK settings.   

### Add serialbox and rest_framework to INSTALLED_APPS
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'serialbox',
    'rest_framework',
]

from serialbox.serialbox_settings import REST_FRAMEWORK
```

## Configure Database Access
See the [Django Docs](https://docs.djangoproject.com/en/dev/ref/databases/) for
instructions on how to set up database access in your *settings.py* file.  Make
sure to reference the proper documentation for the version of Django you are running.
*The link above is to the current development version.*

>**Note:** SerialBox will run fine on the default **SQLite** database if you want to configure
a more robust database at a later point in time.

## Production Configuration Considerations

### Add your STATIC_FILES configuration
Django requires a destination to install any static files for a given project
like SerialBox- these files include, style sheets, javascript files, etc. 

To get up and running quickly, you can have Django collect the files into 
the root directory of your project by putting the following in your 
*settings.py* file.

**EXAMPLE**
```python

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#...or

STATIC_ROOT = '/var/www/static/serialbox/'

```
>Make sure to set the static folder according to where your web server will
expect static files to be located.  The above is used as an example.

For more on the STATIC_ROOT setting and configuring Django to serve static
files see:

* [STATIC_ROOT](https://docs.djangoproject.com/en/dev/ref/settings/#std%3asetting-STATIC_ROOT)
* [Managing Static Files](https://docs.djangoproject.com/en/dev/howto/static-files/)

### Collect Static Files

Execute the following command in your project root to have Django collect
all of the SerialBox static files into your declared static directory:

    python manage.py collectstatic

### Set DEBUG to False and Configure Allowed Hosts
If you are installing into a production environment, make sure your 
`DEBUG` setting in your `settings.py` file is set to `False` and that the 
[ALLOWED_HOSTS](https://docs.djangoproject.com/en/1.9/ref/settings/#allowed-hosts)
setting is configured according to your environment.


## Add Serialbox URLS to your urls.py Module

```
from django.conf.urls import url, include
from serialbox.api import urls

urlpatterns = [
    url(r'^serialbox/', include(urls)),
]
```

## Run Migrations
Running your Django migrations will populate your configured database with 
the tables needed for SerialBox and Django.
```
python manage.py makemigrations
python manage.py migrate
```

## Create The Default Permissions and Groups
You will need to create the default permissions that the API checks
during inbound `allocate` requests.  In addition, this command will
create some default convenience groups that allow you to quickly give
users access to the Pool, Region and Allocate APIs.

    python manage.py load_serialbox_auth


## (Optional) Execute the Unit Tests

### Using Your Settings File
You can execute the SerialBox unit tests using the settings that you configured
in the steps above.  If, for some reason, the tests fail try using the supplied
settings file in the instructions in the next section below.
```
python manage.py test serialbox
```

### ...Or Using the Provided Test Settings File
The SerialBox unit tests can be run independently using a sqlite database
by executing the unit tests as in the example below:
```
python manage.py test serialbox --settings=serialbox.tests.settings
```

Your SerialBox installation should be complete at this point.  You can
run the Django development server to test or hook into your favorite
web server.  For more on running and configuring Django see the
[The Django Project web site.](http://www.thedjangoproject.com)
