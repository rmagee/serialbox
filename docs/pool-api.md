# Pool API
The Pool API is the primary means by which number range *Pools* are configured
and managed within *SerialBox*.  

## General Usage
The general theme behind the *SerialBox* RESTful API is pretty standard across
most of the system.  

### General URL Format Patterns
When executing an API, you'll need to format the URL properly the URL format for
almost all *SerialBox* API end-points as follows:


```
    http[s]://[servername]:[port]/[path]/[api name]/[variables]/?format=[format]&[querstring-var]=[querysting-val]...
```

**URL Values**

*  `servername` the host name or IP address of SerialBox host

*  `port`  The TCP port SerialBox is being hosted on.  If you are using
standard HTTP or HTTPS this is not required.

* `path`  The path you configured for the SerialBox app in your *urls.py* file
during the installation and setup process.  **Note**: If the SerialBox API is configured
to be at the root then the `path` portion, as specified in this document, 
should be omitted in your URLs.

* `api name` The name of the API you are calling

* `variables` One or more variables that the API will be expecting

* `format` By default the ``xml``, ``json`` and ``csv`` formats
are enabled.  However, this is primarily a fucntion of your
[Django Rest Framework](http://www.django-rest-framework.org>) configuration.
See the [Django Rest Framework](http://www.django-rest-framework.org>) documentation
on [Renderers](http://www.django-rest-framework.org/api-guide/renderers/>) for
more info.

* `querystring-var` and `querystring-val` These are standard HTTP query-string
arguments that are optional and vary from one API function to the next.  Each
API function that has any custom query-string paramters will have
them documented accordingly.

> > ***Related Reponses***
The *SerialBox* API *Pool* and *Region* functions support returning
their child-parent reference information as hyperlinks.  To enable hyperlinked
replies, ass the query-string parameter `related=true` to your API URLs
as necessary.

## The SerialBox Pool API Services

The following APIs will be covered in this section...

| API  | Description   |
|---|---|
|/pools/ | lists all pools currently configured.|
|/pool-create/ | used to create new pools.|
|/pool-detail/ | used to retreive information about specific pools.|
|/pool-modify/ | used to modify existing pools.|
|/pool-form/ | used to render an HTML form that can be used to create, display or modify a pool.|

## Listing Available Pools

### URL

The API for listing all available pools is located at:

    http[s]://[host]:[port]/[path]/pools/

For example:

    https://mydomain.org:9982/serialbox/pools/


By default, the system will return all pool values in a self-documented HTML
format with JSON returns embedded in the markup.  To have a pure JSON or XML
serialized return specify xml either of the following mime types in the HTTP
request Content-Type header field:

* `application/json`
* `application/xml`

**OR** specify your return value markup in the `format=[value]` where value
can be:

* xml - xml formatted return
* json - JSON formatted return
* api - HTML formatted API page with documentation, etc.
* csv - Comma separated values.

**Format Example** where the format querystring variable can be any of the
items in the list above.  This example using *json*.

    http://myserver:8888/api/pools/?format=json


## Getting A Specific Pool's Detail
Returns info on a specific pool if a valid pool's machine_name is supplied
within the request URL. 

### URL 

    http[s]://[host]:[port]/[path]/pool-detail/[machine_name]/

For example, to retrieve detail on pool with machine name *mypool*:

    https://mydomain.org:9982/serialbox/pool-detail/mypool/


### HTTP Methods Supported
*    GET - Will return the field info for a given Pool instance.

### Query Parameters

* `related` If you would like the related Regions to come back as
Hyperlinked Relations, pass in a query parameter of related and set
it to true.
* `format` The format parameters depend on your *Django Rest Framework*
configuration and can be found on the API page listed under the **GET**
button at the left upper side of each page.

### Return Fields

* `sequentialretion_set`: a list of *sequential regions* associated with the
pool.  Other types of regions are available if your SerialBox installation
has different *Flavor Packs* installed.  
* `created_date`: Text.  The date the pool record was created.  Time zone can vary
according to your Django config.  ISO 8601 format.
* `modified_date`: Text.  The date the pool record was last modified.  Time zone can
vary according to your Django config.  ISO 8601 format.
* `readable_name`: Text.  The human readable name of the pool.
* `machine_name`: Text.  The machine name of the pool.  This is used as the unique
identifier for the pool in system-to-system API messages, etc.
* `active`: Boolean.  Whether the pool instance is active or not.  Inactive pools can 
not return number data via API calls.
* `request_threshold`: Integer.  The maximum range size that a pool can return when
engaged in API number allocation execution.

**Example**
```json
{
   "sequentialregion_set": [],
   "created_date": "2016-04-12T20:23:13.063788Z",
   "modified_date": "2016-04-12T20:23:13.063896Z",
   "readable_name": "created by unit test",
   "machine_name": "utpool1",
   "active": true,
   "request_threshold": 100
}
```


------------------
## Creating New Pools

### URL

The API for creating new pools can be accessed via the following URL:

    http[s]://[host]:[port]/[path]/pool-create/


### HTTP Methods Supported
* POST - Posting a JSON serialized Pool will result in the creation of a new
pool within SerialBox.

### Details

Below is an example JSON object that, when posted to the SerialBox *pool-create*
API will result in the creation of a new pool.

```javascript
{
    "readable_name": "My Pool",
    "machine_name": "mypool",
    "active": true,
    "request_threshold": 1000
}
```

### Required Fields 

When creating new pools it is required that the following three fields be present
during the execution of the API call:

* `readable_name`: Text.  The human readable name of the pool.
* `machine_name`: Text.  The URL-safe machine name of the pool.  This is used as the unique
identifier for the pool in system-to-system API messages, etc.
* `request_threshold`: Integer.  the maximum range size that a pool can return when
engaged in API number allocation execution.

### Optional Fields

* `active`: Boolean.  Whether the pool instance is active or not.  Inactive pools can 
not return number data via API calls.

>**Note**: The boolean `active` field default value is `true`.  If you wish to create
an inactive pool, you must specify this value explicitly.

---
## Modifying and Deleting Pools

### HTTP Methods Supported
* PUT - using the HTTP PUT method will result in SerialBox using 
the provided serialized JSON *Pool* data to update an existing pool specified
in by *machine_name* in the URL.
* DELETE - using the HTTP DELETE method will result in the deletion of a 
number pool.

### URL

To modify and delete pools, use the following URL:

    http[s]://[host]:[port]/[path]/pool-modify/[pool machine_name]

For example:

    https://mydomain.org:9982/serialbox/pool-modify/mypool/

### Modification
You can modify any of the [required fields](#required-fields) that are used 
to create pools by referencing an existing pool's machine name in the URL and
including any fields to be updated in a PUT body.  

For example, to change the *active* property of a pool named *utpool1*, one 
would HTTP PUT the following JSON to the pool-modify API with *utpool1*
specified in the URL.  For example:

**Example Content**

    {
        "active": false
    }
    
**Example URL**

    https://localhost:8000/pool-modify/utpool1/

To change multiple field values, one could include many at once as below where the 
pool would be marked to active and the readable name would be changed.

** Example Content **

    {
      "readable_name": "changed readable name",
      "active": true
    }

### Deleting Pools

Deleting pools is fairly straight forward.  By executing the `pool-modify` API
along with an HTTP method of DELETE, one can delete a Pool record by supplying
it's *machine_name* value in the last value of the URL as below:

**Example URL**

    https://localhost:8000/pool-modify/utpool1/

> **NOTE:** The return value for this call will be an HTTP 204
