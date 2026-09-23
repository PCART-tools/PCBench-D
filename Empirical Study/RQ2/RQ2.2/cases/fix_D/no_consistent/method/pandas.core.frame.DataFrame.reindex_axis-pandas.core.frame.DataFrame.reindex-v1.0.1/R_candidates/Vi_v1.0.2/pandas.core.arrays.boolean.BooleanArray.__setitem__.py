    def __setitem__(self, key, value):
        _is_scalar = is_scalar(value)
        if _is_scalar:
            value = [value]
        value, mask = coerce_to_array(value)

        if _is_scalar:
            value = value[0]
            mask = mask[0]

        key = check_array_indexer(self, key)
        self._data[key] = value
        self._mask[key] = mask
