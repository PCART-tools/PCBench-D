    def __getitem__(self, key):
        if isinstance(self._info_axis, MultiIndex):
            return self._getitem_multilevel(key)
        return super(Panel, self).__getitem__(key)
