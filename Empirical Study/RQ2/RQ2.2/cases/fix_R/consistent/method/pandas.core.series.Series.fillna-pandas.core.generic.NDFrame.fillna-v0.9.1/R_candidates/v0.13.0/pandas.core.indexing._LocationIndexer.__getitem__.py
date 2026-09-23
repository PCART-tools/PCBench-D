    def __getitem__(self, key):
        if type(key) is tuple:
            return self._getitem_tuple(key)
        else:
            return self._getitem_axis(key, axis=0)
