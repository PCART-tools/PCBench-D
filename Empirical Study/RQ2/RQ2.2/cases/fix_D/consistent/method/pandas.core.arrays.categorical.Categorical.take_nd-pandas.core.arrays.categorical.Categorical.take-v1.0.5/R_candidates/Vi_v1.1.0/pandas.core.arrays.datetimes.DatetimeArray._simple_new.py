    @classmethod
    def _simple_new(cls, values, freq=None, dtype=DT64NS_DTYPE):
        assert isinstance(values, np.ndarray)
        if values.dtype != DT64NS_DTYPE:
            assert values.dtype == "i8"
            values = values.view(DT64NS_DTYPE)

        result = object.__new__(cls)
        result._data = values
        result._freq = freq
        result._dtype = dtype
        return result
