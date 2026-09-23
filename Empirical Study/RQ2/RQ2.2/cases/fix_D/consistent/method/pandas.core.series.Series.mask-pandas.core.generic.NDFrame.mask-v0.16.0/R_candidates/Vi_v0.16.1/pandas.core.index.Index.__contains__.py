    def __contains__(self, key):
        hash(key)
        # work around some kind of odd cython bug
        try:
            return key in self._engine
        except TypeError:
            return False
