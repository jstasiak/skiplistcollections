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


def test_skiplistdict_boolean_value():
    d = SkipListDict()
    eq_(bool(d), False)
    d[1] = 2
    eq_(bool(d), True)
    del d[1]
    eq_(bool(d), False)


def test_level_drops_down_when_deleting_stuff():
    d = SkipListDict()

    counter = 0
    while d.level < 4:
        d[counter] = counter
        counter += 1

    for key in list(d.keys()):
        del d[key]

    eq_(d.level, 0)


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


def test_skiplistset_boolean_value():
    s = SkipListSet()
    eq_(bool(s), False)
    s.add(1)
    eq_(bool(s), True)
    s.remove(1)
    eq_(bool(s), False)


def test_skiplistdict_iteration_regression():
    # The regression would result in yielding more items than necessary
    # if the search key was not found in the dictionary
    sld = SkipListDict()
    sld.update(dict(b='b', d='d'))

    eq_(tuple(sld.keys(start_key='c')), ('d',))
    eq_(tuple(sld.keys(start_key='c', reverse=True)), ('b',))

    eq_(tuple(sld.keys(start_key='e')), ())
    eq_(tuple(sld.keys(start_key='a', reverse=True)), ())
