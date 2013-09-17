import math
import random

from six import PY3
from six.moves import xrange

__version__ = '0.0.1'


class SkipListDict(object):
    def __init__(self, maxsize=65535, random=random.random):
        self._max_level = int(math.log(maxsize, 2))
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

    def _iteritems(self, start_key=None, reverse=False):
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

    def keys(self, start_key=None, reverse=False):
        for k, v in self._iteritems(start_key, reverse):
            yield k

    def values(self, start_key=None, reverse=False):
        for k, v in self._iteritems(start_key, reverse):
            yield v

    if not PY3:
        iteritems = _iteritems
        iteritems.__name__ = 'iteritems'

        def items(self, start_key=None, reverse=False):
            return tuple(self.iteritems(start_key, reverse))

        iterkeys = keys
        iterkeys.__name__ = 'iterkeys'

        def keys(self, start_key=None, reverse=False):
            return tuple(self.iterkeys(start_key, reverse))

        itervalues = values
        itervalues.__name__ = 'itervalues'

        def values(self, start_key=None, reverse=False):
            return tuple(self.itervalues(start_key, reverse))
    else:
        items = _iteritems

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

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False
