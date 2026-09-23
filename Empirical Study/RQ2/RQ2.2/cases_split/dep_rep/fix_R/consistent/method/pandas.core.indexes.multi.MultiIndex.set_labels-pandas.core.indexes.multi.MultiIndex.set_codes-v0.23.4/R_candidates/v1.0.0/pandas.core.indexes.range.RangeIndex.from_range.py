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
                f"{cls.__name__}(...) must be called with object coercible to a "
                f"range, {repr(data)} was passed"
            )

        cls._validate_dtype(dtype)
        return cls._simple_new(data, dtype=dtype, name=name)
