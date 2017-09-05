# SerialBox Documentation

SerialBox solves the non-trivial problem of allocating serial numbers among
many distributed (and often disparate) systems where the non-duplication of serial data is of the utmost
importance.  SerialBox solves this problem by becoming a centralized, easy to 
implement hub where number range pools can be defined and accessed via a clean 
and simple RESTful API.  

## Notes

Serial box was written using the 
[Django](http://www.djangoproject.com) and
[Django Rest Framework](http://django-rest-framework.org) projects.
In order to
understand some of the finer aspects of configuring and deploying SerialBox you should have
some cursory understanding of [Django](http://www.djangoproject.com) and
the [Django Rest Framework](http://django-rest-framework.org).  However, for most 
simple number range operations, SerialBox should function fine out of the box!


## License
SerialBox is distributed and licensed under the 
[GNU General Public License v3](http://www.gnu.org/licenses/gpl-3.0.html)
Copyright (c) 2015 SerialLab LLC, All rights reserved.
