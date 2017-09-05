# Extending SerialBox
SerialBox functionality can be enhanced and extended via pre and post processing
rules and FlavorPacks.

## Rules
SerialBox `rules` are executed before and after each allocation request and 
are specified in a given application's Django Settings module.  The order 
in which rules are executed before and after each allocation API request
is determined in the dictionary and are specified by `Generator`.  See the 
[GENERATOR_PREPROCESSING_RULES](settings/#generator_preprocessing_rules)
documentation. 

If there are no rules specified for pre or post processing using the full
class name of the `Generator` then any `default` rule specifications defined 
in the either rules dictionary will be used.  See the [default pre-processing rules](settings#default)
for an example of how (and what) default rules are declared. 


## FlavorPacks
FlavorPacks are Django Apps that can extend the `pool` API and allow 
SerialBox to serve up types of *number* regions not currently defined. 
In the [Custom FlavorPacks](flavorpacks/) section you will find
a very thorough presentation of this idea.