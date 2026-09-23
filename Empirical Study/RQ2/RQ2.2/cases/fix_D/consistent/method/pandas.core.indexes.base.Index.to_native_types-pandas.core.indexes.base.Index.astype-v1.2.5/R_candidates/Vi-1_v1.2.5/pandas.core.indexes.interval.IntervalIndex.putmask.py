    def putmask(self, mask, value):
        arr = self._data.copy()
        try:
            value_left, value_right = arr._validate_setitem_value(value)
        except (ValueError, TypeError):
            return self.astype(object).putmask(mask, value)

        if isinstance(self._data._left, np.ndarray):
            np.putmask(arr._left, mask, value_left)
            np.putmask(arr._right, mask, value_right)
        else:
            # TODO: special case not needed with __array_function__
            arr._left.putmask(mask, value_left)
            arr._right.putmask(mask, value_right)
        return type(self)._simple_new(arr, name=self.name)
