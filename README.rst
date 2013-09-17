skiplistcollections
===================

.. image:: https://travis-ci.org/jstasiak/skiplistcollections.png?branch=master
   :alt: Build status
   :target: https://travis-ci.org/jstasiak/skiplistcollections

*skiplistcollections* is a Python module containing skip list based sorted collections. *skiplistcollections* is written in Python and works with:

* CPython 2.6+, 3.2+
* PyPy 1.9+


Usage
-----

See http://pythonsweetness.tumblr.com/post/45227295342/fast-pypy-compatible-ordered-map-in-89-lines-of-python for details.

.. code-block:: python

   >>> from skiplistcollections import SkipListDict
   >>> things = SkipListDict(maxsize=16)
   >>> len(things)
   0
   >>> things['x'] = 1
   >>> 'x' in things
   True
   >>> len(things)
   1
   >>> things['g'] = 2
   >>> things['z'] = 3
   >>> tuple(things.keys())
   ('g', 'x', 'z')
   >>> tuple(things.values())
   (2, 1, 3)
   >>> tuple(things.items())
   (('g', 2), ('x', 1), ('z', 3))
   >>> del things['z']
   >>> len(things)
   2

Copyright
---------

Original version - Copyright (C) 2013 David Wilson

Copyright (C) 2013 Jakub Stasiak

This source code is licensed under MIT license, see LICENSE file for details.
