    @classmethod
    def _simple_new(cls, values, freq=None, dtype=_TD_DTYPE):
        assert dtype == _TD_DTYPE, dtype
        assert isinstance(values, np.ndarray), type(values)

        result = object.__new__(cls)
        result._data = values.view(_TD_DTYPE)
        result._freq = to_offset(freq)
        result._dtype = _TD_DTYPE
        return result
