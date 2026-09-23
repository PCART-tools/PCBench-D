    def __getitem__(self, key):
        if isinstance(key, tuple):
            key = tuple(com._apply_if_callable(x, self.obj) for x in key)
        else:
            # scalar callable may return tuple
            key = com._apply_if_callable(key, self.obj)

        if type(key) is tuple:
            return self._getitem_tuple(key)
        else:
            return self._getitem_axis(key, axis=0)
