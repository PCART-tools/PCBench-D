    def __setitem__(self, key, value):
        self._check_frozen()
        self._state[key] = value
