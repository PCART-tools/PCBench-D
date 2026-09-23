    def __init__(self, values, mask, copy=False):
        if not (isinstance(values, np.ndarray) and is_integer_dtype(values.dtype)):
            raise TypeError(
                "values should be integer numpy array. Use "
                "the 'integer_array' function instead"
            )
        if not (isinstance(mask, np.ndarray) and is_bool_dtype(mask.dtype)):
            raise TypeError(
                "mask should be boolean numpy array. Use "
                "the 'integer_array' function instead"
            )

        if copy:
            values = values.copy()
            mask = mask.copy()

        self._data = values
        self._mask = mask
