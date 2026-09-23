    @classmethod
    def _simple_new(cls, values, name=None, freq=None, tz=None,
                    dtype=None, **kwargs):
        """
        we require the we have a dtype compat for the values
        if we are passed a non-dtype compat, then coerce using the constructor
        """

        if getattr(values, 'dtype', None) is None:
            # empty, but with dtype compat
            if values is None:
                values = np.empty(0, dtype=_NS_DTYPE)
                return cls(values, name=name, freq=freq, tz=tz,
                           dtype=dtype, **kwargs)
            values = np.array(values, copy=False)

        if is_object_dtype(values):
            return cls(values, name=name, freq=freq, tz=tz,
                       dtype=dtype, **kwargs).values
        elif not is_datetime64_dtype(values):
            values = _ensure_int64(values).view(_NS_DTYPE)

        result = object.__new__(cls)
        result._data = values
        result.name = name
        result.offset = freq
        result.tz = timezones.maybe_get_tz(tz)
        result._reset_identity()
        return result
