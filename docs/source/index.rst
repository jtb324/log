.. modified-logger documentation master file, created by
   sphinx-quickstart on Fri Sep 26 17:54:26 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

modified-logger documentation
=============================
Python-based logger intended to enhance the functionality of the standard python logger. Some notable distinctions are summarized below:

*  the addition of an additional logging level, `logging.VERBOSE`, that falls between `logging.INFO` and `logging.DEBUG` level
*  ability to sample logging records based on a proportion threshold given by the user

installing the package:
-----------------------
User can install the logger using the following code:

.. code::

  pip install modified-logger



  
.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   installation
   examples

.. toctree::
   :maxdepth: 2 
   :caption: API
   :hidden:

   api

