import math
import random

try:
    import collections.abc as colabc
except ImportError:
    import collections as colabc

from six.moves import xrange

__version__ = '0.0.4'
__all__ = ('SkipListDict',)


class MappingView(colabc.MappingView):
    def __init__(self, mapping, start_key=None, reverse=False):
        self._mapping = mapping
        self._start_key = start_key
        self._reverse = reverse

        if start_key is None:
            self.__len__ = self._len

    def _len(self):
        return len(self._mapping)

    def __repr__(self):
        return ('{0.__class__.__name__}({0._mapping!r}, start_key={0._start_key})'.format(self))


class KeysView(MappingView, colabc.KeysView):
    def __contains__(self, key):
        assert self._start_key is None
        return key in self._mapping

    def __iter__(self):
        for k, v in self._mapping._items(self._start_key, self._reverse):
            yield k


class ItemsView(MappingView, colabc.ItemsView):
    def __contains__(self, item):
        assert self._start_key is None
        key, value = item
        try:
            v = self._mapping[key]
        except KeyError:
            return False
        else:
            return v == value

    def __iter__(self):
        return self._mapping._items(self._start_key, self._reverse)


class ValuesView(MappingView, colabc.ValuesView):
    def __contains__(self, value):
        assert self._start_key is None
        for v in self._mapping.values():
            if v == value:
                return True

        return False

    def __iter__(self):
        for k, v in self._mapping._items(self._start_key, self._reverse):
            yield v


class SkipListDict(colabc.MutableMapping):
    def __init__(self, capacity=65535, random=random.random):
        self._max_level = int(math.log(capacity, 2))
        self._level = 0
        self._head = self._make_node(self._max_level, None, None)
        self._nil = self._make_node(-1, None, None)
        self._tail = self._nil
        self._head[3:] = [self._nil for x in xrange(self._max_level)]
        self._update = [self._head] * (1 + self._max_level)
        self._p = 1 / math.e
        self._size = 0
        self._random = random

    def _make_node(self, level, key, value):
        node = [None] * (4 + level)
        node[0] = key
        node[1] = value
        return node

    def _random_level(self):
        lvl = 0
        max_level = min(self._max_level, self._level + 1)
        while self._random() < self._p and lvl < max_level:
            lvl += 1
        return lvl

    def _items(self, start_key=None, reverse=False):
        if reverse:
            node = self._tail
        else:
            node = self._head[3]
        if start_key is not None:
            update = self._update[:]
            found = self._find_less(update, start_key)
            if found[3] is not self._nil:
                node = found[3]
        idx = 2 if reverse else 3
        while node[0] is not None:
            yield node[0], node[1]
            node = node[idx]

    def items(self, start_key=None, reverse=False):
        return ItemsView(self, start_key, reverse)

    iteritems = items

    def keys(self, start_key=None, reverse=False):
        return KeysView(self, start_key, reverse)

    iterkeys = keys

    def values(self, start_key=None, reverse=False):
        return ValuesView(self, start_key, reverse)

    itervalues = values

    def _find_less(self, update, key):
        node = self._head
        for i in xrange(self._level, -1, -1):
            current_key = node[3 + i][0]
            while current_key is not None and current_key < key:
                node = node[3 + i]
                current_key = node[3 + i][0]
            update[i] = node
        return node

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        assert key is not None
        update = self._update[:]
        node = self._find_less(update, key)
        prev = node
        node = node[3]

        if node[0] == key:
            node[1] = value
        else:
            lvl = self._random_level()
            self._level = max(self._level, lvl)
            node = self._make_node(lvl, key, value)
            node[2] = prev

            for i in xrange(0, lvl + 1):
                node[3 + i] = update[i][3 + i]
                update[i][3 + i] = node

            if node[3] is self._nil:
                self._tail = node
            else:
                node[3][2] = node

            self._size += 1

    def __delitem__(self, key):
        update = self._update[:]
        node = self._find_less(update, key)
        node = node[3]

        if node[0] == key:
            node[3][2] = update[0]

            for i in xrange(self._level + 1):
                if update[i][3 + i] is not node:
                    break

                update[i][3 + i] = node[3 + i]

            while self._level > 0 and self._head[3 + self._level][0] is None:
                self._level -= 1

            if self._tail is node:
                self._tail = node[2]

            self._size -= 1
        else:
            raise KeyError('Key %r not found' % (key,))

    def __getitem__(self, key):
        node = self._head

        for i in xrange(self._level, -1, -1):
            current_key = node[3 + i][0]

            while current_key is not None and current_key < key:
                node = node[3 + i]
                current_key = node[3 + i][0]

        node = node[3]

        if node[0] == key:
            return node[1]
        else:
            raise KeyError

    def __iter__(self):
        for k, v in self._items():
            yield k

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, dict(self))
