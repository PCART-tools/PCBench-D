    def __getitem__(self, key):
        if type(key) is tuple:
            key = tuple(com._apply_if_callable(x, self.obj)
                        for x in key)
            try:
                values = self.obj._get_value(*key)
                if is_scalar(values):
                    return values
            except Exception:
                pass

            return self._getitem_tuple(key)
        else:
            # we by definition only have the 0th axis
            axis = self.axis or 0

            key = com._apply_if_callable(key, self.obj)
            return self._getitem_axis(key, axis=axis)
