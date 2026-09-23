    def putmask(self, mask, value) -> Index:
        mask, noop = validate_putmask(self._data, mask)
        if noop:
            return self.copy()

        try:
            self._validate_fill_value(value)
        except (ValueError, TypeError):
            dtype = self._find_common_type_compat(value)
            return self.astype(dtype).putmask(mask, value)

        arr = self._data.copy()
        arr.putmask(mask, value)
        return type(self)._simple_new(arr, name=self.name)
