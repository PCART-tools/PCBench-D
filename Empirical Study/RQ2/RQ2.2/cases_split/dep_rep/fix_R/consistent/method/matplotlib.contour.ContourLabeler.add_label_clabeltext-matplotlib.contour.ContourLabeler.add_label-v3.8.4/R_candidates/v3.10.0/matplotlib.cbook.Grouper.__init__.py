    def __init__(self, init=()):
        self._mapping = weakref.WeakKeyDictionary(
            {x: weakref.WeakSet([x]) for x in init})
        self._ordering = weakref.WeakKeyDictionary()
        for x in init:
            if x not in self._ordering:
                self._ordering[x] = len(self._ordering)
        self._next_order = len(self._ordering)  # Plain int to simplify pickling.
