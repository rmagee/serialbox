## Extending SerialBox Functionality With FlavorPacks

>NOTE: All of the code in this example can be found on the SerialLab GitHub
page under the `sbdemo` package.

### FlavorPack Framework
SerialBox can be extended using a plug-in framework built into the system. 
The plug=in framework is referred to the FlavorPack Framework and allows 
Python modules to be defined and discovered in such a way that they are both
easy to install and easy to use.  A python module that can be installed using 
this framework is referred to as a *FlavorPack*.

### What FlavorPacks Can Do
A FlavorPack can dynamically add SerialBox *Generators* and *Regions* to a
SerialBox application so that the existing SerialBox [Pool API](pool-api.md) 
can continue to function as expected but with new types of *Generators* and 
*Regions* participating.  In addition, a FlavorPack can expose it's own URLS
and APIs as well; however, this is more a function of the 
[Django Rest Framework](django-rest-framework.org) than it is of anything
SerialBox is providing.

## Writing Your Own FlavorPack 

### Dependencies
SerialBox requires [Django](http://djangoproject.org) and the 
[Django Rest Framework](django-rest-framework.org)...as such, your FlavorPacks
project will require these as well.


### Create a New Django Project With a New App.
Pretty straight forward.  If you don't know how to do this, check out the 
Django website and refresh your skills.  

### Define Your Custom Regions
SerialBox *Regions* are, in their most basic sense, just Django models that 
inherit from the `serialbox.models.Region` class.  

FlavorPacks can define custom regions that follow different rules than the 
default `SequentialRegions` that are part of the standard install.  For example,
there are *RandomizedRegions* currently available in the *Random Flavorpack*.
All custom regions should inherit from the `serialbox.models.Region` class and
will inherit the following properties:

* `pool` If a Sequential Region is related to a `Pool`, the machine name
of the pool or a related URL value will be in the `Pool` field.  To return
related pools as URLs see the *Related Responses* notes at the top of this page.
* `created_date`: Text.  The date the sequential-region record was created.  Time zone can vary
according to your Django config.  ISO 8601 format.
* `modified_date`: Text.  The date the sequential-region record was last modified.  Time zone can
vary according to your Django config.  ISO 8601 format.
* `readable_name`: Text.  The human readable name of the sequential-region.
* `machine_name`: Text.  The machine name of the sequential-region.  This is used as the unique
identifier for the pool in system-to-system API messages, etc.
* `active`: Boolean.  Whether the sequential region is active or not.  Inactive regions can 
not return number data via API calls.
* `order`: Integer.  The order of a region determines its behavior within pools
where there is more than one region defined.  For example, if there are two
regions defined, when number requests are granted they will be taken from the 
first active pool with the lowest *order* defined.  

For this example we will define a `WordRegion` class that will help us keep 
track of words as we cycle through the English language dictionary file typically
provided on POSIX compliant operating systems (more on this later).

##### WordRegion Class Definition

    from django.db import models
    from django.utils.translation import gettext_lazy as _
    
    import serialbox.models as sb_models
    
    
    class WordRegion(sb_models.Region):
        '''
        A word region generates lists of words from a language dictionary.
        '''
        last_word_line = models.IntegerField(
            verbose_name=_('Last Word Line'),
            help_text=_('The line number of the last word issued '
                        'maintains the state of the word based region.'),
            default=1)


As you can see, the `WordRegion` class inherits from the default `Region` class
and, in addition, implements a single `CharField` field that is used to store the 
last word issued by the system.


### Define a Generator Package 
Create a new package called `generators` in your project root.  Within that
project create a module named `word` and add the `WordGenerator` class if you 
are following along with the tutorial.  

#### Create a Custom Generator
A SerialBox `Generator` knows how to utilize a *Region* to return a list of 
*numbers*.  I put the term numbers 
here in italics because, in reality, a generator could return a list of anything.
There's no contract in the SerialBox framework that prevents generators from 
returning the same number twice or from even spitting out words from the dictionary
for example...which is exactly what we'll do in this example/tutorial.  

What happens to the list a generator creates?  It ends up in the *numbers* element
of the [Allocation API](allocate.md) response...even if the generator isn't 
technically generating *numbers*.


#### Example Custom WordGenerator
The word generator below will grab lines form the *words* file on a POSIX 
compliant system and return the amount specified in the `size` parameter.
**Note that the WordGenerator calls `Generator.set_number_list`
 before it exits.**

    import linecache
    from serialbox.generators.common import Generator
    
    
    class WordGenerator(Generator):
        '''
        This generator will create lists of words from the
        '''
    
        def generate(self, request, response, region, size):
            # change this to use a different file
            filename = '/usr/share/dict/words'
            # get that last word line from the region
            first = region.last_word_line
            # grab the n number of lines after that word based
            # on the size of the request
            lines = []
            max_line = first + size
            for lineno in range(first, max_line):
                lines.append(linecache.getline(filename, lineno).strip())
            # just for fun set the encoding to us-english using the ISO code
            response.encoding = 'en-US'
            # set the state of the region to the last line
            region.last_word_line = max_line
            # always call set_number_list in generators by passing
            # in the list of (whatever) you've generated
            return self.set_number_list(response, lines)


>> **IMPORTANT** In case you missed it above...
Make sure you call the `Generator.set_number_list` function
and pass it whatever list you are generating for whatever flavor pack 
Generator you may be working on.  If you do not do this, the list
will not be appended to the response!

#### A Note About Rules
All `generators` in the SerialBox framework load their pre and post processing 
rules in the `Generator.__init__` method.  See below.  If your `Generator`
instance will fail using the `default` rules defined in the `serialbox_settings`
module then override the `__init__` method appropriately or set your
django settings file like below.

    from serialbox.serialbox_settings import GENERATOR_PREPROCESSING_RULES
    
    GENERATOR_PREPROCESSING_RULES[
            'sbdemo.words_flavorpack.generators.words.WordGenerator'    
        ] = []
        
For the purposes of this example `WordGenerator`, however, the default pre-processing
and post-processing
rules will work just fine.

### Create an API Package.
In order for your FlavorPack to be a good SerialBox citizen, it needs to participate 
in the SerialBox Pool API by not only supplying serial number data but also
by reporting back any information relative to `Regions` defined in a SerialBox
system that are based on those defined in your FlavorPack.  We will go into 
this more later...

In any event, create a new package named `api` in the root of your application.
This is where you will define the 
Django Rest Framework 
[Serializers](http://www.django-rest-framework.org/api-guide/serializers/) and
your [ViewSets](http://www.django-rest-framework.org/api-guide/viewsets/) that
will be responsible for sharing the data relative to your FlavorPack's Region
and Number Allocation data. In
addition, you will place the [URL configurations](https://docs.djangoproject.com/en/dev/topics/http/urls/)
relative to these assets here as well.  This **IS NOT JUST BEST PRACTICE**, 
SerialBox makes certain assumptions about your application's structure during 
the FlavorPack discovery process and the API directory should always be directly
under your root folder in a module named `api`.

#### Define your ViewSets
Within your API package, create a viewsets.py file/module.  Here we will define
the DjangoRestFramework ViewSets that will be used to expose our WordRegions
for serialization via the SerialBox API.  For more on Django Rest Framework 
ViewSets see [Django Rest Framework ViewSets](http://www.django-rest-framework.org/api-guide/viewsets/).
Our ViewSet will allow for WordRegions to be individually retrieved,
listed, updated and deleted via the SerialBox API. 

A ViewSet is basically a more simplified Django class-based View which represents the "V" in 
a standard MVC architecture.  As in the example below, our ViewSet will tell
Django what model we are serializing, what `serializer` class to use and allows
us to define different views based on the ViewSet for different HTTP methods such
as POST, GET, PUT, DELETE.  All of this with the intent of exposing our FlavorPack's 
configuration data to the outside world via the SerialBox API.
The views defined at the bottom will be referenced
later in our *urls.py* configuration.  
        
    from rest_framework import viewsets, renderers
    
    from serialbox.api.viewsets import FormMixin
    
    from sbdemo.words_flavorpack.models import WordRegion
    from sbdemo.words_flavorpack.api import serializers
    
    
    class WordRegionViewSet(viewsets.ModelViewSet, FormMixin):
        queryset = WordRegion.objects.all()
        lookup_field = 'machine_name'
    
        def get_serializer_class(self):
            '''
            Return a different serializer depending on the client request.
            '''
            ret = serializers.WordRegionSerializer
            try:
                if self.request.query_params.get('related') == 'true':
                    ret = serializers.HyperlinkedWordRegionSerializer
            except AttributeError:
                pass
            return ret
    
    
    word_region_list = WordRegionViewSet.as_view({
        'get': 'list'
    })
    word_region_create = WordRegionViewSet.as_view({
        'post': 'create'
    })
    word_region_detail = WordRegionViewSet.as_view({
        'get': 'retrieve'
    })
    word_region_modify = WordRegionViewSet.as_view({
        'put': 'partial_update',
        'delete': 'destroy'
    })
    word_region_form = WordRegionViewSet.as_view({
        'get': 'form'
    })


#### Add a urls.py To the API Package
This is a standard Django URLs module that tells Django (and the DjangoRestFramework)
what views/viewsets we are exposing.  For more on Django URLS see 
[Django URLS](https://docs.djangoproject.com/en/dev/topics/http/urls/).

Basically, what we are going to do here is expose the ViewSets we defined.  
Take special note of the fact that we supplied names for each of the `url` 
configurations...specifically the `word-region-list` `url`.  This name 
will be configured later in our FlavorPack's Django AppConfig class in the section below.

    from django.conf.urls import url
    
    from sbdemo.words_flavorpack.api import viewsets
    
    urlpatterns = [
        url(r'^word-regions/$',
            viewsets.word_region_list,
            name='word-region-list'),
        url(r'^word-region-create/$',
            viewsets.word_region_create,
            name='word-region-create'),
        url(r'^word-region-detail/(?P<machine_name>[0-9a-zA-Z]{1,100})/$',
            viewsets.word_region_detail,
            name='word-region-detail'),
        url(r'^word-region-modify/(?P<machine_name>[0-9a-zA-Z]{1,100})/$',
            viewsets.word_region_modify,
            name='word-region-modify'),
        url(r'^word-region-form/(?P<machine_name>[0-9a-zA-Z]{1,100})/$',
            viewsets.word_region_form,
            name='word-region-form'),
    ]



#### Declare Your Pool Fields and Serializers
Create a `serializers` module in your `api` package.  For your `Pool` fields.

A FlavorPack will dynamically add it's *Regions* to the SerialBox `Pool` API
when you install it; however, to do this you need to tell SerialBox what 
fields to add by declaring them somewhere.  SerialBox expects you to declare
two types of fields for the API- a `SlugRelatedField` and a `HyperLinkRelatedField`.
(Both of these types of fields are specific to the *Django Rest Framework*.)
The slug field will allow your regions to be represented in the `Pool` API by 
their `machine_name` field and the hyperlinked field will allow your regions
to be represented as URLs that link directly to the region detail API in your
*FlavorPack*.  Since the primary purpose of these fields is for serialization,
they are typically declared in an `api.serializers` module. 

Serializers are used in the SerialBox API to return information about the 
current state of your Regions.  To be clear, the serializers we are defining 
now are *not* serializing word data (that's the job of our `Generator`) but, rather, serializing 
the `WordRegion` Django Model we have defined earlier.  SerialBox exposes the
state of all Regions and Pools as part of its standard API and FlavorPacks 
must do this as well. 

For the most part, you won't need to do much with your serializers other than
declare them and set the Django model reference.  See the example below.

    from rest_framework import serializers as rf_serializers
    from serialbox.api.serializers import RegionSerializer
    from sbdemo.words_flavorpack.models import WordRegion
    
    
    from sbdemo.words_flavorpack import models
    
    ##
    # These fields will be added to the pool serializer automatically since
    # they are specified in the pool_slug_fields and the pool_hyperlinked_fields
    # values in the words_flavorpack.apps.WordsFlavorpackConfig module.
    ##
    wordregion_set = rf_serializers.SlugRelatedField(
        many=True,
        queryset=models.WordRegion.objects.all(),
        slug_field='machine_name',
        required=False
    )
    
    wordregion_hyperlink_set = rf_serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='word-region',
        lookup_field='machine_name',
    )
    
    
    class WordRegionSerializer(RegionSerializer):
        '''
        Specifies the model...excludes the id...
        '''
        class Meta(object):
            model = WordRegion
            exclude = ('id',)
    
    
    class HyperlinkedWordRegionSerializer(WordRegionSerializer):
        '''
        Addst the hyperlinked field...
        '''
        pool = rf_serializers.HyperlinkedRelatedField(view_name='pool-detail',
                                                      read_only=True,
                                                      lookup_field='machine_name')

The first thing we do is create a standard `RegionSerializer` that 
specifies in its `Meta` class what Django Model will be serialized. In our example,
the model being used is the `WordRegion` that we defined earlier. This
first serializer, if you look above, only specifies the Model and (optionally)
to remove the database primary-key *id* field from any serialized data.

The next thing you need is to create a serializer class that inherits from your
first class and add the `Pool` field as above.  This will be used when
clients access the SerialBox API and request that related pools be returned
as URL values as opposed to the machine name of a related pool.  If you do not
do this, your FlavorPack will raise an exception when clients ask for URL values
in the serialized model data.  

### Implement the FlavorPackApp
The final step in getting SerialBox to recognize your FlavorPack is to implement
an instance of the `serialbox.flavor_packs.FlavorPackApp`- which is an extension of a 
[Django AppConfig](https://docs.djangoproject.com/en/1.10/ref/applications/)
that uses a custom Meta class to perform some 
self-registration of URLs, Generators and fields within FlavorPacks.

Create an apps.py/apps module in your application root directory.  
This is really just a Django best practice.  It will allow other developers
to know where your FlavorPackApp is declared.

Within your create a class that implements the `FlavorPackApp`.  Within this class
you will do the following 4 things:

1.  Declare the name of the FlavorPackApp- this is the full path to the 
class as it sits within your python package.
2.  Declare your `pool_slug_fields` and your `pool_hyperlink_fields` properties.  
This is done by creating a property
called pool_slug_fields- see the example code below.  Here you will be telling
SerialBox how to append your Region's related fields to Pool model instances. 
You will return a dictionary with the name of the field and the full path to 
the field within your project.  If you look in the example below, this relates
exactly to the fields we declared above in the 
[Declare Your Pool Fields and Serializers](#declare-your-pool-fields-and-serializers) 
section.
3.  Declare your Generator.  This is how SerialBox knows where to find the 
`Generator` class you declared in the [Define a Generator Package](#define-a-generator-package)
step above.
4.  Tell SerialBox what `url` name to use in order to list any of the 
FlavorPack's custom Regions.  For our example, this is the URL defined with the name
*word-region-list* in the
[Add a urls.py To the API Package](#add-a-urlspy-to-the-api-package) step above.


#### FlavorPackApp example:

    from serialbox.flavor_packs import FlavorPackApp

    class WordsFlavorpackConfig(FlavorPackApp):
        # The flavorpack app is a django AppConfig instance
        # with a meta-class that does some auto-registration for flavorpacks...
        # for more on AppConfigs see the Django documentation.
        name = 'sbdemo.words_flavorpack'
    
        @property
        def pool_slug_fields(self):
            return {
                'wordregion_set':
                'sbdemo.words_flavorpack.api.serializers.wordregion_set'
            }
    
        # Each flavorpack must supply hyperlink fields for it's serializer fields
        @property
        def pool_hyperlink_fields(self):
            return {
                'wordregion_set':
                'sbdemo.words_flavorpack.api.serializers.wordregion_hyperlink_set'
            }
        # Each flavorpack must supply number generators for it's regions
    
        @property
        def generators(self):
            # here we define the model and generator that
            # is responsible for creating words for the API and maintaining
            # the appropriate state in the database
            return {
                'sbdemo.words_flavorpack.models.WordRegion':
                'sbdemo.words_flavorpack.generators.words.WordGenerator'
            }
    
        @property
        def api_urls(self):
            # this is the name of the URL config that returns word regions,
            # returning it makes it visible on the self-documenting
            # django rest framework HTML interface at the Root Api page...
            return ['word-region-list']


