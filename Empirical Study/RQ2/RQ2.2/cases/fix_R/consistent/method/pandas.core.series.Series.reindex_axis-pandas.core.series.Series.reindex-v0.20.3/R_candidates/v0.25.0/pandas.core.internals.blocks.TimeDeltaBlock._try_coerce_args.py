    def _try_coerce_args(self, other):
        """
        Coerce values and other to int64, with null values converted to
        iNaT. values is always ndarray-like, other may not be

        Parameters
        ----------
        other : ndarray-like or scalar

        Returns
        -------
        base-type other
        """

        if is_valid_nat_for_dtype(other, self.dtype):
            other = tslibs.iNaT
        elif is_integer(other) and other == tslibs.iNaT:
            pass
        elif isinstance(other, (timedelta, np.timedelta64)):
            other = Timedelta(other).value
        elif hasattr(other, "dtype") and is_timedelta64_dtype(other):
            other = other.astype("i8", copy=False).view("i8")
        else:
            # coercion issues
            # let higher levels handle
            raise TypeError(other)

        return other
