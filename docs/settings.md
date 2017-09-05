## Intro

The `serialbox.serialbox_settings` module has some default settings for 
the SerialBox framework that can be overriden in your Django `settings`
module.  In addition, there are some default settings for the 
[Django Rest Framework](http://django-rest-framework.org) that you can utilize.

## The .env file environment variables
The following environment variables are used to populate the database settings
in the DATABASES section of the SerialBox Django settings.py file.

SERIALBOX_USER
SERIALBOX_PASSWORD
SERIALBOX_DB
SERIALBOX_DB_HOST
SERIALBOX_DB_PORT


## The SerialBox Django Rest Framework Settings
SerialBox makes some assumptions about how you may want it to behave.  If you 
want to take advantage of these import the default `REST_FRAMEWORK` settings
variable into your Django `settings` module as in the example below:


    from serialbox.serialbox_settings import REST_FRAMEWORK
    
>> ![warning](warning.png)WARNING: Make sure to declare the `REST_FRAMEWORK`
variable before any existing modifications the Django Rest Framework settings or
those settings will be overwritten should they overlap with the default 
SerialBox `REST_FRAMEWORK` settings.

The default Django Rest Framework settings that are included by default are
the inclusion of the JSON, Browsable API, XML, and CSV renderers in addition
to the JSON, Form, XML and CSV parsers. If you 
do not require all of these formats, feel free to configure the REST_FRAMEWORK
dictionary accordingly.  These settings are only included as a convenience.  

The default page size for data is set to 20 and the default authentication
classes are limited to Basic Auth and Session Auth...again...only as a 
convenience.

The default settings are below:

    REST_FRAMEWORK.update({
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
            'rest_framework_xml.renderers.XMLRenderer',
            'rest_framework_csv.renderers.CSVRenderer',
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
            'rest_framework_xml.parsers.XMLParser',
        ),
        'PAGE_SIZE': 20,
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    })

## SerialBox Default Configuration Settings

Use the following settings to custom configure SerialBox and the SerialBox API.
They can be overriden in your application's django `settings` module if required.


## SB_POOL_API_LIST_LIMIT

   **Type**: Integer

   **Default**: 1000

   Set this value to limit the amount of items that can be returned by the pool detail API.
   It is highly unlikely that you would have more than 1000 number pools defined...but, if you
   do and you notice they're not returning back from the PoolList API then you'll need
   to set the value to an appropriate size.



## GENERATOR_PREPROCESSING_RULES

   **Type**: Dictionary

   **Default**: See below

   Set this value to assign preprocessing rules to specific Generators.
   The dictionary is defined as the full class name of the Generators that you wish
   to assign the Rules to with each assigned a list of Generators to apply in order.
   See the Rules section for more info.

### Default
```
GENERATOR_PREPROCESSING_RULES = {
        'default': [
            'serialbox.rules.limits.ActiveRule',
            'serialbox.rules.limits.RequestThresholdLimitRule',
        ],
        'serialbox.generators.sequential.SequentialGenerator': [
            'serialbox.rules.limits.ActiveRule',
            'serialbox.rules.limits.SizeLimitRule',
            'serialbox.rules.limits.RequestThresholdLimitRule',
        ]
    })
```

## GENERATOR_POSTPROCESSING_RULES
**Type**: Dictionary

**Default**: Empty Dictionary

Set the value to assign post-processing rules to a specific Generator.  The
declared order of the rules should be according to how you intend them to
be executed during serial number generation.  For more on rules, see the Rules
section of the SerialBox documentation.

Default:
```
'GENERATOR_POSTPROCESSING_RULES',
    {}
```
