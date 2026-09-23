    def __delitem__(self, key):
        # TODO: Do we want to deprecate deleting spines?
        del self._dict[key]
