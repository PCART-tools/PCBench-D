class _OrderedSet(collections.abc.MutableSet):
    def __init__(self):
        self._od = collections.OrderedDict()

    def __contains__(self, key):
        return key in self._od

    def __iter__(self):
        return iter(self._od)

    def __len__(self):
        return len(self._od)

    def add(self, key):
        self._od.pop(key, None)
        self._od[key] = None

    def discard(self, key):
        self._od.pop(key, None)
