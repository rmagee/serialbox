
## Pre and Post Processing Rules
SerialBox gives you the ability to customize and extend it's functionality
via pre and post-processing rules.  Rules are exectued in the order in which 
they are configured and are also organized by [*Generator*](basic_concepts.md#generators).  
Generators are classes that are responsible for generating serial number data.  As such, they 
handle discrete serial number requests within which rules can be applied.  Out
of the box, SerialBox only has one default *Generator* which is the Sequential
Generator.  However, other FlavorPacks may add different *Generators* with 
different *Rules*...such as, for example, a randomized generator or a list 
based generator, etc.  


### Types of Rules
Processing Rules are executed at two points during the processing of a 
number allocation request and come in two flavors:

*   Pre-Processing Rules
*   Post-Processing Rules


### Pre-Processing Rules

Pre-processing rules are executed *prior* to any requests being executed by any of
the SerialBox *Generators*.  A pre-processing rule is a simple python class 
that either returns silently or raises a `serialbox.rules.errors.RuleError` with
a message with regards to why the rule failed.


The default pre-processing rules for each type of Generator are set in your
django settings file under the GENERATOR_PREPROCESSING_RULES section in the 
settings document.  More on this in the 
[tutorial below](#step-2-modify-your-settings-file).
    

### Post-Processing Rules

Post-processing rules, as the name would imply, are executed after the SerialBox
Generators have put together a serial number response *but before any database
transactions have been committed* so it is still possible to throw an error here
and rollback any requests that have passed through the full request phase.  However,
this **totally depends on database support for transactions**.  If you need
to be 100% certain that numbers will not be allocated within a request that 
violates a custom rule, you must implementa a 
[Pre-processing Rule](#pre-processing-rules).

