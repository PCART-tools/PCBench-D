    def __getitem__(self, key):
        try:
            return self._dict[key]
        except TypeError:
            pass
        for k, v in self._pairs:
            if k == key:
                return v
        raise KeyError(key)
