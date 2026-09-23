    def _maybe_coerce_values(self, values):
        """Input validation for values passed to __init__. Ensure that
        we have datetime64ns, coercing if necessary.

        Parameters
        ----------
        values : array-like
            Must be convertible to datetime64

        Returns
        -------
        values : ndarray[datetime64ns]

        Overridden by DatetimeTZBlock.
        """
        if values.dtype != _NS_DTYPE:
            values = conversion.ensure_datetime64ns(values)
        return values
