    def __delitem__(self, key):
        self._check_frozen()
        del self._state[key]
