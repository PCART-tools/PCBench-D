    @classmethod
    def _simple_new(cls, values, name=None, freq=None, **kwargs):
        values = np.array(values, copy=False)
        if values.dtype == np.object_:
            values = libts.array_to_timedelta64(values)
        if values.dtype != _TD_DTYPE:
            values = _ensure_int64(values).view(_TD_DTYPE)

        result = object.__new__(cls)
        result._data = values
        result.name = name
        result.freq = freq
        result._reset_identity()
        return result
