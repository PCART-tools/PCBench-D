    def __getitem__(self, key):
        key = _apply_if_callable(key, self)

        if isinstance(self._info_axis, MultiIndex):
            return self._getitem_multilevel(key)
        if not (is_list_like(key) or isinstance(key, slice)):
            return super(Panel, self).__getitem__(key)
        return self.loc[key]
