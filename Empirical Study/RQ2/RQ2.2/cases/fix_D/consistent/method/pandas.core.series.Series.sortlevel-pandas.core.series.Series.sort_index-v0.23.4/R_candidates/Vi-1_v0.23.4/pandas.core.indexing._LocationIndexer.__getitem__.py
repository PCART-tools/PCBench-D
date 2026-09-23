    def __getitem__(self, key):
        if type(key) is tuple:
            key = tuple(com._apply_if_callable(x, self.obj)
                        for x in key)
            try:
                if self._is_scalar_access(key):
                    return self._getitem_scalar(key)
            except (KeyError, IndexError):
                pass
            return self._getitem_tuple(key)
        else:
            # we by definition only have the 0th axis
            axis = self.axis or 0

            maybe_callable = com._apply_if_callable(key, self.obj)
            return self._getitem_axis(maybe_callable, axis=axis)
