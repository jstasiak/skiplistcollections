import math
import random

try:
    import collections.abc as colabc
except ImportError:
    import collections as colabc

from six.moves import xrange

__version__ = '0.0.6'
__all__ = ('SkipListDict',)


class MappingView(colabc.MappingView):
    def __init__(self, mapping, start_key=None, reverse=False):
        self._mapping = mapping
        self._start_key = start_key
        self._reverse = reverse

    def __len__(self):
        if self._start_key is not None:
            # hacky workaround, if start_key is specified we have no way of knowing
            # the result size at the moment
            return len(tuple(iter(self)))

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


NODE_KEY = 0
NODE_VALUE = 1
NODE_PREVIOUS_NODE = 2
NODE_NEXT_NODE = 3


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
        self._capacity = capacity

    @property
    def capacity(self):
        return self._capacity

    @property
    def level(self):
        return self._level

    def _make_node(self, level, key, value):
        node = [None] * (4 + level)
        node[NODE_KEY] = key
        node[NODE_VALUE] = value
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
            node = self._head[NODE_NEXT_NODE]
        if start_key is not None:
            update = self._update[:]
            node = self._find_less(update, start_key)

            if node[NODE_KEY] is not None:
                if node[NODE_KEY] < start_key:
                    node = node[NODE_NEXT_NODE]

                if reverse and node[NODE_KEY] > start_key:
                    node = node[NODE_PREVIOUS_NODE]

        idx = NODE_PREVIOUS_NODE if reverse else NODE_NEXT_NODE

        while node[NODE_KEY] is not None:
            yield node[NODE_KEY], node[NODE_VALUE]
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
            current_key = node[NODE_NEXT_NODE + i][0]
            while current_key is not None and current_key < key:
                node = node[NODE_NEXT_NODE + i]
                current_key = node[NODE_NEXT_NODE + i][NODE_KEY]
            update[i] = node
        return node

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        assert key is not None
        update = self._update[:]
        node = self._find_less(update, key)
        prev = node
        node = node[NODE_NEXT_NODE]

        if node[NODE_KEY] == key:
            node[NODE_VALUE] = value
        else:
            lvl = self._random_level()
            self._level = max(self._level, lvl)
            node = self._make_node(lvl, key, value)
            node[NODE_PREVIOUS_NODE] = prev

            for i in xrange(0, lvl + 1):
                node[NODE_NEXT_NODE + i] = update[i][NODE_NEXT_NODE + i]
                update[i][NODE_NEXT_NODE + i] = node

            if node[NODE_NEXT_NODE] is self._nil:
                self._tail = node
            else:
                node[NODE_NEXT_NODE][NODE_PREVIOUS_NODE] = node

            self._size += 1

    def __delitem__(self, key):
        update = self._update[:]
        node = self._find_less(update, key)
        node = node[NODE_NEXT_NODE]

        if node[NODE_KEY] == key:
            node[NODE_NEXT_NODE][NODE_PREVIOUS_NODE] = update[0]

            for i in xrange(self._level + 1):
                if update[i][NODE_NEXT_NODE + i] is not node:
                    break

                update[i][NODE_NEXT_NODE + i] = node[NODE_NEXT_NODE + i]

            while self._level > 0 and self._head[NODE_NEXT_NODE + self._level][NODE_KEY] is None:
                self._level -= 1

            if self._tail is node:
                self._tail = node[NODE_PREVIOUS_NODE]

            self._size -= 1
        else:
            raise KeyError('Key %r not found' % (key,))

    def __getitem__(self, key):
        node = self._find_less(self._update[:], key)[NODE_NEXT_NODE]

        if node[NODE_KEY] == key:
            return node[NODE_VALUE]
        else:
            raise KeyError

    def __iter__(self):
        for k, v in self._items():
            yield k

    def __repr__(self):
        return '{0.__class__.__name__}({1}, capacity={0._capacity})'.format(
            self,
            '{' + ', '.join('{0!r}: {1!r}'.format(k, v) for (k, v) in self.items()) + '}')


class SkipListSet(colabc.MutableSet):
    def __init__(self, **kwargs):
        self._storage = SkipListDict(**kwargs)

    def __contains__(self, key):
        return key in self._storage

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)
        pass

    def add(self, key):
        self._storage[key] = None

    def discard(self, key):
        del self._storage[key]

    def __repr__(self):
        return '{0.__class__.__name__}({1!r}, capacity={0._storage.capacity})'.format(
            self, tuple(self))
