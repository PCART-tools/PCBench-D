    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError(key)

        return getattr(self, key)
