    def _try_coerce_args(self, values, other):
        """
        Coerce values and other to int64, with null values converted to
        iNaT. values is always ndarray-like, other may not be

        Parameters
        ----------
        values : ndarray-like
        other : ndarray-like or scalar

        Returns
        -------
        base-type values, base-type other
        """
        values = values.view('i8')

        if isinstance(other, bool):
            raise TypeError
        elif is_null_datetimelike(other):
            other = tslibs.iNaT
        elif isinstance(other, (timedelta, np.timedelta64)):
            other = Timedelta(other).value
        elif hasattr(other, 'dtype') and is_timedelta64_dtype(other):
            other = other.astype('i8', copy=False).view('i8')
        else:
            # coercion issues
            # let higher levels handle
            raise TypeError(other)

        return values, other
