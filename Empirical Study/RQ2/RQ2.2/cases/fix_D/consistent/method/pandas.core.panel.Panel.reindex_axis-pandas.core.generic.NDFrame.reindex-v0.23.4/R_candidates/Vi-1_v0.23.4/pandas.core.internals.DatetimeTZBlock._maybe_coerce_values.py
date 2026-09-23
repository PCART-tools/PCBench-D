    def _maybe_coerce_values(self, values, dtype=None):
        """Input validation for values passed to __init__. Ensure that
        we have datetime64TZ, coercing if necessary.

        Parametetrs
        -----------
        values : array-like
            Must be convertible to datetime64
        dtype : string or DatetimeTZDtype, optional
            Does a shallow copy to this tz

        Returns
        -------
        values : ndarray[datetime64ns]
        """
        if not isinstance(values, self._holder):
            values = self._holder(values)

        if dtype is not None:
            if isinstance(dtype, compat.string_types):
                dtype = DatetimeTZDtype.construct_from_string(dtype)
            values = values._shallow_copy(tz=dtype.tz)

        if values.tz is None:
            raise ValueError("cannot create a DatetimeTZBlock without a tz")

        return values
