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
        base-type values, base-type other
        """

        values = values.view('i8')

        if isinstance(other, bool):
            raise TypeError
        elif is_null_datetimelike(other):
            other = tslibs.iNaT
        elif isinstance(other, (datetime, np.datetime64, date)):
            other = self._box_func(other)
            if getattr(other, 'tz') is not None:
                raise TypeError("cannot coerce a Timestamp with a tz on a "
                                "naive Block")
            other = other.asm8.view('i8')
        elif hasattr(other, 'dtype') and is_datetime64_dtype(other):
            other = other.astype('i8', copy=False).view('i8')
        else:
            # coercion issues
            # let higher levels handle
            raise TypeError(other)

        return values, other
