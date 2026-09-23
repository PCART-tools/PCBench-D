    @classmethod
    def _simple_new(cls, values, name=None, freq=None, **kwargs):
        """
        Values can be any type that can be coerced to Periods.
        Ordinals in an ndarray are fastpath-ed to `_from_ordinals`
        """
        if not is_integer_dtype(values):
            values = np.array(values, copy=False)
            if len(values) > 0 and is_float_dtype(values):
                raise TypeError("PeriodIndex can't take floats")
            return cls(values, name=name, freq=freq, **kwargs)

        return cls._from_ordinals(values, name, freq, **kwargs)
