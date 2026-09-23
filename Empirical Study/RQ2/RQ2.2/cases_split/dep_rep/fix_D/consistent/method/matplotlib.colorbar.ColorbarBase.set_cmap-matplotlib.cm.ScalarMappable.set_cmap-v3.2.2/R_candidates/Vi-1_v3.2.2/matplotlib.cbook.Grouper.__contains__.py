    def __contains__(self, item):
        return weakref.ref(item) in self._mapping
