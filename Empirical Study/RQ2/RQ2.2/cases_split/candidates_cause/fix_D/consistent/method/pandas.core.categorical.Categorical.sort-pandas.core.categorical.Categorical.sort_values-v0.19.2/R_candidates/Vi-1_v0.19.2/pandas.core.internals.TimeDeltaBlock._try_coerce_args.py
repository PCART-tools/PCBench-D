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
        base-type values, values mask, base-type other, other mask
        """

        values_mask = isnull(values)
        values = values.view('i8')
        other_mask = False

        if isinstance(other, bool):
            raise TypeError
        elif is_null_datelike_scalar(other):
            other = tslib.iNaT
            other_mask = True
        elif isinstance(other, Timedelta):
            other_mask = isnull(other)
            other = other.value
        elif isinstance(other, np.timedelta64):
            other_mask = isnull(other)
            other = Timedelta(other).value
        elif isinstance(other, timedelta):
            other = Timedelta(other).value
        elif isinstance(other, np.ndarray):
            other_mask = isnull(other)
            other = other.astype('i8', copy=False).view('i8')
        else:
            # scalar
            other = Timedelta(other)
            other_mask = isnull(other)
            other = other.value

        return values, values_mask, other, other_mask
