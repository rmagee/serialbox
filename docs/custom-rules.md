# Custom Rules
Here you will find a tutorial on implementing custom pre and post processing
rules for any `Generator` class.

## Step 1. Implement a PreProcessingRule Class
Rules are very simple to both create and configure for use in SerialBox.
Start by creating a class that inherits from `serialbox.rules.common.PreProcessingRule`
or `serialbox.rules.common.PostProcessingRule` (if you want do do post-processing of 
requests).  

Override/implement the `execute` method on the base class which takes the 
following arguments:
    
*   `request` - The Django Rest Framework (HTTP) Request object.
*   `pool` - The `serialbox.models.Pool` instance from which 
numbers are being requested.
*   `region` - The `serialbox.models.SequentialRegion` from which numbers 
are being requested.
*   `size` - an integer representing the size of the request.

In addition, if you require a custom error message or HTTP status be returned
to your client then create a custom error class that inherits from the
`serialbox.rules.errors.RuleError` and specify a custom return message along
with, if needed, an HTTP status that applies to the error.  The default 
HTTP status for the `RuleError` is HTTP 400 BAD REQUEST.

The example below is an implementation of a PreProcessingRule class
that checks request sizes and raises a custom exception when the a number allocation
request specifies an odd number of serial numbers.

### Example Custom Rule and Error Classes


    from rest_framework import status
    from serialbox.rules.common import PreprocessingRule
    from serialbox.rules.errors import RuleError


    class OddNumberError(RuleError):
    
        def __init__(self, detail=None):
            self.default_detail = ('No odd number requests are allowed! '
                                   'To disable this remove the OddNumberError '
                                   'rule from the GENERATOR_PREPROCESSING_RULES settings.')
            # NOTE:
            # the status is 400 by default, just including here as an example!!!
            self.status_code = status.HTTP_400_BAD_REQUEST
            RuleError.__init__(self, detail=detail)
    
    
    class NoOddRequests(PreprocessingRule):
        '''
        Example rule that doesn't allow requests for odd numbers.
        '''
    
        def execute(self, request, pool, region, size):
            # check the size
            if size % 2 != 0:
                raise OddNumberError()




Override/implement the `execute` method on the base class which takes the 
following arguments:

*   `request` - The Django Rest Framework (HTTP) Request object.
*   `pool` - The `serialbox.models.Pool` instance from which 
numbers are being requested.
*   `region` - The `serialbox.models.SequentialRegion` from which numbers 
are being requested.
*   `size` - an integer representing the size of the request.

3.  Add the fully qualified class name of your python class to the *SequentialGenerator*
list of the SerialBox GENERATOR_PREPROCESSING_RULES dictionary.

>NOTE: Make sure your class is on the python path and, in addition, make sure
you don't forget to add the existing (default) rules by concatenating the 
existing rule settings with any custom ones.  See the settings example below
and the [SerialBox settings](settings.md) section for more.

## Step 2. Modify your Settings File
In your Django settings file, you will want to import either  `GENERATOR_PREPROCESSING_RULES`
or `GENERATOR_POSTPROCESSING_RULES` depending on what type of rule you are
implementing.  This is done so that you can import the default SerialBox
rule implementation and add your rule to it.  However, this is only necessary
if you wish to implement all of the default rules (which is usually a good idea)...
but, by all means, feel free to implement only the rules you wish to.

### Example Settings Entry
```python

from serialbox.serialbox_settings import GENERATOR_PREPROCESSING_RULES

GENERATOR_PREPROCESSING_RULES['serialbox.generators.sequential.SequentialGenerator'] = \
    GENERATOR_PREPROCESSING_RULES['serialbox.generators.sequential.SequentialGenerator'] + \
    ['sbdemo.odd_number_rule.NoOddRequests']                                     

```
Restart your server and execute an odd-numbered request against one of your 
pools and you should get the error defined in the custom error class.