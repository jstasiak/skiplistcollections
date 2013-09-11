from random import randint

from nose.tools import eq_, ok_
from six.moves import xrange

from skiplistcollections import SkipListDict


def test_regular_stuff():
    stuff = SkipListDict(maxsize=1024)

    used_keys = set((0,))

    for count in xrange(1000):
        eq_(len(stuff), count)
        eq_(len(tuple(stuff.keys())), count)
        eq_(len(tuple(stuff.values())), count)
        eq_(len(tuple(stuff.items())), count)

        items = tuple(stuff.items())
        if items:
            previous_key, previous_value = items[0]
            for k, v in items[1:]:
                eq_(v, k % 100)
                ok_(k > previous_key, '%r should be greater than %r' % (k, previous_key))
                previous_key = k

        number = 0
        while number in used_keys:
            number = randint(0, 1000000)

        used_keys.add(number)

        ok_(number not in stuff)

        stuff[number] = number % 100

        ok_(number in stuff)
        eq_(stuff[number], number % 100)
