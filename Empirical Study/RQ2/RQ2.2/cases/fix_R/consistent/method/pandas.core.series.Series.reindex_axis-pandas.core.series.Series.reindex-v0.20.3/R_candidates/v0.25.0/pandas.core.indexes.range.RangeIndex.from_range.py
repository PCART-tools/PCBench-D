    @classmethod
    def from_range(cls, data, name=None, dtype=None):
        """
        Create RangeIndex from a range object.

        Returns
        -------
        RangeIndex
        """
        if not isinstance(data, range):
            raise TypeError(
                "{0}(...) must be called with object coercible to a "
                "range, {1} was passed".format(cls.__name__, repr(data))
            )

        cls._validate_dtype(dtype)
        return cls._simple_new(data, dtype=dtype, name=name)
