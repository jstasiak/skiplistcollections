skiplistcollections
===================

.. image:: https://travis-ci.org/jstasiak/skiplistcollections.png?branch=master
   :alt: Build status
   :target: https://travis-ci.org/jstasiak/skiplistcollections

*skiplistcollections* is a Python module containing skip list based sorted collections. *skiplistcollections* is written in Python and works with:

* CPython 2.6+, 3.2+
* PyPy 1.9+

Project page on GitHub: https://github.com/jstasiak/skiplistcollections

Project page on PyPI: https://pypi.python.org/pypi/skiplistcollections

SkipListDict
------------

``SkipListDict`` is container providing dict-like interface and implemented using skip list. It's permanently sorted by key.

* Iterating the container (starting with any key, supports reverse ordering) is *O(n)*
* Getting, setting and deleting arbitrary key is *O(log n)* on average, *O(n)* in worst case (degenerated skip list)

See http://pythonsweetness.tumblr.com/post/45227295342/fast-pypy-compatible-ordered-map-in-89-lines-of-python for details.

.. code-block:: python

   >>> from skiplistcollections import SkipListDict
   >>> things = SkipListDict(capacity=16)
   >>> len(things)
   0
   >>> things['x'] = 1
   >>> things.setdefault('x', 'DEFAULT')
   1
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
   >>> tuple(things.items(start_key='x'))
   (('x', 1), ('z', 3))
   >>> tuple(things.items(start_key='x', reverse=True))
   (('x', 1), ('g', 2))
   >>> del things['z']
   >>> things.update({'a': 'A', 'b': 'B'})
   >>> len(things)
   4
   >>> things
   SkipListDict({'a': 'A', 'b': 'B', 'g': 2, 'x': 1}, capacity=16)


As you can see, ``SkipListDict`` follows Python dict interface quite closely. In fact it inherits ``MutableMapping`` Abstract Base Class.

There are differences of course:

* You need to set the maximum dict size when you create it
* Initializing using another mapping is not supported yet
* You can't use None as a key
* ``items``, ``keys``, and ``values`` are views and accept ``start_key`` and ``reverse`` parameters

SkipListSet
-----------

``SkipListSet`` is set implementation  using skip list. It's permanently sorted by key.

* Iterating the container is *O(n)*
* Adding, removing and checking if a key exist in the containe is *O(log n)* on average, *O(n)* in worst case (degenerated skip list)

.. code-block:: python

   >>> from skiplistcollections import SkipListSet
   >>> things = SkipListSet(capacity=16)
   >>> len(things)
   0
   >>> things.add(3)
   >>> len(things)
   1
   >>> things.add(1)
   >>> things.add(4)
   >>> things
   SkipListSet((1, 3, 4), capacity=16)
   >>> tuple(things)
   (1, 3, 4)
   >>> things.remove(2)
   Traceback (most recent call last):
   KeyError: 2



Changes
--------

0.0.6
`````
* Fixed bug with SkipListDict yielding too many items if start_key was not found (GitHub issue #1)

0.0.5
`````

* Fixed SkipListDict repr
* Created SkipListSet

0.0.4
`````

* Included start_key and reverse values in views reprs
* Improved README


0.0.3
`````

* ``items()``, ``values()``, ``keys()`` return views now

0.0.2
`````

* Improved README


Copyright
---------

Original version - Copyright (C) 2013 David Wilson

Copyright (C) 2013 Jakub Stasiak

This source code is licensed under MIT license, see LICENSE file for details.
