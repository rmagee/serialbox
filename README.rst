SerialBox
=========

.. image:: https://gitlab.com/serial-lab/serialbox/badges/master/coverage.svg
   :target: https://gitlab.com/serial-lab/serialbox/pipelines
.. image:: https://gitlab.com/serial-lab/serialbox/badges/master/pipeline.svg
   :target: https://gitlab.com/serial-lab/serialbox/commits/master
.. image:: https://badge.fury.io/py/serialbox.svg
    :target: https://badge.fury.io/py/serialbox

.. code-block:: text

  ____            _       _ ____            
 / ___|  ___ _ __(_) __ _| | __ )  _____  __
 \___ \ / _ \ '__| |/ _` | |  _ \ / _ \ \/ /
  ___) |  __/ |  | | (_| | | |_) | (_) >  <
 |____/ \___|_|  |_|\__,_|_|____/ \___/_/\_\


Unique Numbers Across Systems
-----------------------------

SerialBox solves the non-trivial problem of generating and distributing serial
number information from system to system for the use in manufacturing and
supply chain environments. SerialBox was built with Marijuana and
Pharmaceutical production and distribution systems in mind but can be
used for any application that requires a unique serial number distribution API.

Open, Simple, Tested and Well Documented
----------------------------------------

SerialBox is easy to install, provides a simple RESTful API for fast and
clean implementation, comes with a comprehensive suite of unit tests and
is fully documented.

Easily Extended
---------------
Need a custom number output format?  Need to generate a customized region of
numbers or characters in a specific format for a specific goal?  The
SerialBox is easily extended via the *FlavorPack* plugin framework and there
is an example flavorpack implementation and instructions available in the
*SerialBox Documentation*.  In addition, you can write *pre-processing* and
*post-processing* python modules that can be easily configured to handle
inbound and outbound messages.

Example FlavorPack
------------------
The SerialBox documentation outlines how to develop a *FlavorPack* plugin for
SerialBox- you can find the example from the documentation here:

https://gitlab.com/serial-lab/sbdemo/

Get Serial
----------
SerialBox is distributed via the code on this site under the GPLv3 license
and also via the gitlab docker registry.

Docker Compose Project
----------------------
Check out the docker compose project here:

https://gitlab.com/serial-lab/serial-box-docker-compose

Documentation
-------------
Installation and configuration instructions can be found here:

https://serial-lab.gitlab.io/serialbox/


