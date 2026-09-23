    def __setitem__(self, key, value):
        # TODO: Do we want to deprecate adding spines?
        self._dict[key] = value
