    def _try_coerce_args(self, values, other):
        """
        localize and return i8 for the values

        Parameters
        ----------
        values : ndarray-like
        other : ndarray-like or scalar

        Returns
        -------
        base-type values, base-type other
        """
        # asi8 is a view, needs copy
        values = _block_shape(values.view("i8"), ndim=self.ndim)

        if isinstance(other, ABCSeries):
            other = self._holder(other)

        if isinstance(other, bool):
            raise TypeError
        elif is_datetime64_dtype(other):
            # add the tz back
            other = self._holder(other, dtype=self.dtype)

        elif is_null_datetimelike(other):
            other = tslibs.iNaT
        elif isinstance(other, self._holder):
            if other.tz != self.values.tz:
                raise ValueError("incompatible or non tz-aware value")
            other = _block_shape(other.asi8, ndim=self.ndim)
        elif isinstance(other, (np.datetime64, datetime, date)):
            other = tslibs.Timestamp(other)
            tz = getattr(other, 'tz', None)

            # test we can have an equal time zone
            if tz is None or str(tz) != str(self.values.tz):
                raise ValueError("incompatible or non tz-aware value")
            other = other.value
        else:
            raise TypeError(other)

        return values, other
