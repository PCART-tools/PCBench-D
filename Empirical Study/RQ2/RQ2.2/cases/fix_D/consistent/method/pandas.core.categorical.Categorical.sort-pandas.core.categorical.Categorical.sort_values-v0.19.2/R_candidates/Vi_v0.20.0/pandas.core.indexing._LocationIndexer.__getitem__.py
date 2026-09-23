    def __getitem__(self, key):
        if type(key) is tuple:
            key = tuple(com._apply_if_callable(x, self.obj) for x in key)
            try:
                if self._is_scalar_access(key):
                    return self._getitem_scalar(key)
            except (KeyError, IndexError):
                pass
            return self._getitem_tuple(key)
        else:
            key = com._apply_if_callable(key, self.obj)
            return self._getitem_axis(key, axis=0)
