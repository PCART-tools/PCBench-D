    def __setitem__(self, key, value) -> None:
        key = check_array_indexer(self, key)

        if is_scalar(value):
            if is_valid_na_for_dtype(value, self.dtype):
                self._mask[key] = True
            else:
                value = self._validate_setitem_value(value)
                self._data[key] = value
                self._mask[key] = False
            return

        value, mask = self._coerce_to_array(value, dtype=self.dtype)

        self._data[key] = value
        self._mask[key] = mask
