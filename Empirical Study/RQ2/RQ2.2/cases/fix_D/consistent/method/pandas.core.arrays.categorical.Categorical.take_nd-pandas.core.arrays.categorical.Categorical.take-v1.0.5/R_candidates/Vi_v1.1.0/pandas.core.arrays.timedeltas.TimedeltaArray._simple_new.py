    @classmethod
    def _simple_new(cls, values, freq=None, dtype=TD64NS_DTYPE):
        assert dtype == TD64NS_DTYPE, dtype
        assert isinstance(values, np.ndarray), type(values)
        if values.dtype != TD64NS_DTYPE:
            assert values.dtype == "i8"
            values = values.view(TD64NS_DTYPE)

        result = object.__new__(cls)
        result._data = values
        result._freq = to_offset(freq)
        result._dtype = TD64NS_DTYPE
        return result
