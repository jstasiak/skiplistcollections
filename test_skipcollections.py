from random import randint

from nose.tools import eq_, ok_
from six.moves import xrange

from skiplistcollections import SkipListDict, SkipListSet


def test_general_skiplistdict_behaviour():
    stuff = SkipListDict(capacity=1024)

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
        try:
            stuff[number]
            assert False, 'Should have raised an exception'
        except KeyError:
            pass

        stuff[number] = number % 100

        ok_(number in stuff)
        eq_(stuff[number], number % 100)

    used_keys.remove(0)

    for key in set(used_keys):
        used_keys.remove(key)

        ok_(key in stuff)
        del stuff[key]
        ok_(key not in stuff)

        eq_(len(stuff), len(used_keys))


def test_general_skiplistset_behaviour():
    stuff = SkipListSet(capacity=1024)

    used_keys = set((0,))

    for count in xrange(1000):
        eq_(len(stuff), count)

        items = tuple(stuff)
        if items:
            previous_key = items[0]
            for k in items[1:]:
                ok_(k > previous_key, '%r should be greater than %r' % (k, previous_key))
                previous_key = k

        number = 0
        while number in used_keys:
            number = randint(0, 1000000)

        used_keys.add(number)

        ok_(number not in stuff)

        stuff.add(number)

        ok_(number in stuff)

    used_keys.remove(0)

    for key in set(used_keys):
        used_keys.remove(key)

        ok_(key in stuff)
        stuff.remove(key)
        ok_(key not in stuff)

        try:
            stuff.remove(key)
            assert False, 'Should have raised an exception'
        except KeyError:
            pass

        eq_(len(stuff), len(used_keys))
