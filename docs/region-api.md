# The Sequential Region API
The following section describes the APIs in place that allow you to list, get,
 create, modify and delete Sequential Regions in SerialBox.

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
---------------

## Sequential Region API Services

The following APIs will be covered in this section:

| API  | Description   |
|---|---|
|/sequential-regions/  |List all Sequential Regions   |
|/sequential-region-create/   |Create a new Sequential Region   |
|/sequential-region-detail/   |Get the detail for a specific Sequential Region   |
|/sequential-region-modify/   |Modify an already existing region's values.   |
|/sequential-region-form/   |Get a specific Sequential Region expressed as and HTML form.|

## Listing Available Sequential Regions

>It is important to remember here that if you need to get all of the 
Sequential Regions within a given pool that calling the pool-detail API will
return this value as an array under the `sequential-regions` key in the return.

### URL

The URL format for listing all available Sequential Regions is located as follows:

    http[s]://[host]:[port]/[path]/sequential-regions/

For example:

    https://mydomain.org:9982/serialbox/sequential-regions/


By default, the system will return all Sequential Region values in a self-documented HTML
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

    http://myserver:8888/api/sequential-regions/?format=json


----------------------------
## Getting Sequential Region Detail

To retrieve all of the data relative to a specific Sequential Region from the system,
use the following endpoint: 

### URL

    http[s]://[host]:[port]/[path]/sequential-region-detail/[machine-name]/
    
For example:

    https://mydomain.org:9982/serialbox/sequential-regions/mytestregion/?format=json
    
### Methods Supported
*   GET - Will return all field info for a given Sequential Region

### Query Parameters

* `related` If you would like the related Pools to come back as
Hyperlinked Relations, pass in a query parameter of related and set
it to true.
* `format` The format parameters depend on your *Django Rest Framework*
configuration and can be found on the API page listed under the **GET**
button at the left upper side of each page.

### Return Fields

* `pool` If a Sequential Region is related to a *Pool*, the machine name
of the pool or a related URL value will be in the *pool* field.  To return
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
* `start`: Integer.  Each Sequential Region must define its boundaries via 
start and end values.  The start value is the first number in the region when
considering a region as a range.
* `end`: Integer. The end value denotes the last number of the region.
* `state`: Integer. The state is the *current* number of the region.  So, for
example, if a new number allocation request were received by the system, the 
system would use the state as the first number in the reply.  After each 
number allocation request, the state is updated to reflect the last known
state plus the size of the last request plus one.  

### Example Response

```javascript
{
    "pool": "my_test_pool",
    "created_date": "2016-04-25T22:20:50.162531Z",
    "modified_date": "2016-04-25T22:20:50.162568Z",
    "readable_name": "My Test Region",
    "machine_name": "mytestregion",
    "active": true,
    "order": 1,
    "start": 1,
    "end": 10000000,
    "state": 1
}
```

---
## Creating a Sequential Region

The service exposed for creating new Sequential Regions can be accessed
via the URL below.

### URL 

    http[s]://[host]:[port]/[path]/sequential-region-create/
    
For example:

    https://myserialbox.mydomainname.com/sequential-region-create/

The following fields are required in the posted JSON or XML data:

*   pool
*   readable_name
*   machine_name
*   start


```javascript
{
    "pool": "mytestpool",
    "readable_name": "My Test Region",
    "machine_name": "mytestregion",
    "active": true,
    "order": 1,
    "start": 1,
    "end": 100,
    "state": 1
}
```

### HTTP Methods Supported
* POST - Posting a serialized Sequential Region (XML or JSON) will result in 
the creation of a new Sequential Region in SerialBox.  

---
## Modifying and Deleting Sequential Regions
Updating a region can be done by accessing the following resource:

### URL

    http[s]://[host]:[port]/[path]/sequential-region-update/[machine_name]
    
For example:

    https://myserialbox.mydomainname.com/sequential-region-update/my-test-region
    
### Modifying

To update a given region, specify the *machine_name* of the region in the URL
as in the example above and add the fields you wish to change/update in the 
HTTP message body.  For example, if you wished to deactivate a specific region,
you would post the active field set to false as below:

```json
{
    "active": false,
}
```

### Deleting
There is no need to for any message body when deleting a *Sequential Region*.
Specify the machine_name of the region you wish to delete and execute the API
call with an HTTP DELETE method specified.  This call will return no body or
message and will have an HTTP status code of 204.


### HTTP Methods Supported
* PUT - Posting a serialized Sequential Region (XML or JSON) will result in 
the creation of a new Sequential Region in SerialBox.  
* DELETE - Executing the API with an HTTP DELETE method specified will remove
the *Sequential Region* specified in the *machine_name* portion of the URL.

> NOTE: The DELETE method will return an HTTP 204 status.
    


