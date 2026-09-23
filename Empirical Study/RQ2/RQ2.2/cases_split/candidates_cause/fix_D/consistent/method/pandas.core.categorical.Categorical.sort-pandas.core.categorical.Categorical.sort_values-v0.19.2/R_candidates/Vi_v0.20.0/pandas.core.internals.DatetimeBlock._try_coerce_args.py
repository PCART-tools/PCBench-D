    def _try_coerce_args(self, values, other):
        """
        Coerce values and other to dtype 'i8'. NaN and NaT convert to
        the smallest i8, and will correctly round-trip to NaT if converted
        back in _try_coerce_result. values is always ndarray-like, other
        may not be

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
        elif isinstance(other, (datetime, np.datetime64, date)):
            other = self._box_func(other)
            if getattr(other, 'tz') is not None:
                raise TypeError("cannot coerce a Timestamp with a tz on a "
                                "naive Block")
            other_mask = isnull(other)
            other = other.asm8.view('i8')
        elif hasattr(other, 'dtype') and is_integer_dtype(other):
            other = other.view('i8')
        else:
            try:
                other = np.asarray(other)
                other_mask = isnull(other)

                other = other.astype('i8', copy=False).view('i8')
            except ValueError:

                # coercion issues
                # let higher levels handle
                raise TypeError

        return values, values_mask, other, other_mask
