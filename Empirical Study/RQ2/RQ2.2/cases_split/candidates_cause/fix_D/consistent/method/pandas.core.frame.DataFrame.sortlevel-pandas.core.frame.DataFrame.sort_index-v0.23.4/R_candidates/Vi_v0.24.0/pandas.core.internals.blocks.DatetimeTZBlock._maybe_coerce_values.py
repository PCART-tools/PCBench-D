    def _maybe_coerce_values(self, values):
        """Input validation for values passed to __init__. Ensure that
        we have datetime64TZ, coercing if necessary.

        Parametetrs
        -----------
        values : array-like
            Must be convertible to datetime64

        Returns
        -------
        values : DatetimeArray
        """
        if not isinstance(values, self._holder):
            values = self._holder(values)

        if values.tz is None:
            raise ValueError("cannot create a DatetimeTZBlock without a tz")

        return values
