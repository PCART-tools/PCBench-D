    def __contains__(self, item):
        return ref(item) in self._mapping
