# Allocation API

## Allocate

The *Allocate* API exposes the The Pool Request View- which is the primary 
view by which other systems will access the API for Pool and Region 
number allocation requests.  

### Forming Requests

#### Format

   
The url should be formatted as follows.  See the options table below for more
info. ::

   http[s]://[servername]:[port]/allocate/[pool machine-name]/[size of the request]/?format=[format]


#### Options
  *  `servername` the host name or IP address of SerialBox host
  *  `port`  The TCP port SerialBox is being hosted on.  If you are using standard HTTP or HTTPS this is not required.
  *  `pool machine-name` The machine-name from which the numbers are being requested.
  *  `size of the request` A positive integer value expressing the size of the number block being requested.  This can be throttled by using the *SizeLimitRule* pre-processing rule.
  *  `format` By default the `xml`, `json` and `csv` formats are enabled.  However, this is primarily a fucntion of your [Django Rest Framework](http://www.django-rest-framework.org) configuration. 

#### Example


So, for example, to request 1000 numbers from a SerialBox pool with machine 
name *my-foo-bar* in *JSON*
formatting, on the host *www.foobar.com*, one would format the request url 
as below: ::

```
   http[s]://www.foobar.com/allocate/my-foo-bar/1000/?format=json
```

> **Important Note**: Paging is not active for this view since the number list is an 
attribute of the response object.  



## Handling Responses

SerialBox will return the following response fields in it's default configuration.

** numbers ** 
A list/array of numbers that represent the reply to the request for numbers.
   
**Sequential Replies**
If the request is from a *Pool* defined with *Sequential Regions* then the
reply will be sequntial in nature and will only include two numbers: the first
and last number.  The range is implied via these two numbers and requesting
systems are able to use any number that falls betweent the two.  The first
number will always be lesser than the last.  

**Non-Sequential Replies**
The list will include all of the numbers explicitly defined and will be sized
according to the *size* parameter supplied in the request.  
   
**fulfilled**
   A boolean value representing whether or not SerialBox could fulfill the 
   request.  This value would be false, for example, if a request were made
   for 1000 numbers from a *Pool*/*Region* that only had 500 left.  SerialBox
   will return the 500 numbers with a fullfilled flag set to `false`.
   
**type**
   This will be either `sequential`, `random` or `list`. Sequential will
   always return **two** numbers.  *Random* and *list* will always return 
   a list of numbers sized according to the inbound *size* parameter.

**encoding**
   This will be either `decimal`, `hex` or `base-36`.
   
   *  **decimal**
      A base-10 number with values from 0-9.  In other words, regular old numbers.
   *  **hex**
      A base-16 hexadecimal number with values from 0-9a-f.
   *  **base-36** 
      A base-36 number with values from 0-9a-z.
**region**
   The *machine-name* of the *Region* that furninshed the request within the 
   *Pool* specified in the *pool machine-name* parameter of the request.
**size_granted**
   The size granted.  This will typically be equal to the inbound *size* 
   paramter; however, when the *fulfilled* flag is set to false, this will
   represent the amount of numbers SerialBox was able to return to the client.


### JSON Response Example

    {
    "numbers": "[395, 404]",
    "fulfilled": true,
    "type": "",
    "encoding": "decimal",
    "region": "Test Region Two",
    "size_granted": 10,
    }

   
### XML Response Example

The *root* node is, aptly enough, named **root**.  This is a function of the
[Django Rest Framework](http://django-rest-framework.org) and can be changed
if need be via a custom
[XML renderer](http://www.django-rest-framework.org/api-guide/renderers/).  

    <root>
      <numbers>[985, 994]</numbers>
      <fulfilled>True</fulfilled>
      <type>sequential</type>
      <encoding>decimal</encoding>
      <region>sqr2</region>
      <size_granted>10</size_granted>
    </root>


### CSV Response Example

First line is, effectively, the header.  

    encoding,fulfilled,numbers,region,size_granted,type
    decimal,True,"[995, 1004]",sqr2,10,sequential
