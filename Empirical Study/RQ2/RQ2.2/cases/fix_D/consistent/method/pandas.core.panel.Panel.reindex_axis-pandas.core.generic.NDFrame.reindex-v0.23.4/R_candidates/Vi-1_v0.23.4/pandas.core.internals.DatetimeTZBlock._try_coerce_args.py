    def _try_coerce_args(self, values, other):
        """
        localize and return i8 for the values

        Parameters
        ----------
        values : ndarray-like
        other : ndarray-like or scalar

        Returns
        -------
        base-type values, values mask, base-type other, other mask
        """
        values_mask = _block_shape(isna(values), ndim=self.ndim)
        # asi8 is a view, needs copy
        values = _block_shape(values.asi8, ndim=self.ndim)
        other_mask = False

        if isinstance(other, ABCSeries):
            other = self._holder(other)
            other_mask = isna(other)

        if isinstance(other, bool):
            raise TypeError
        elif (is_null_datelike_scalar(other) or
              (is_scalar(other) and isna(other))):
            other = tslib.iNaT
            other_mask = True
        elif isinstance(other, self._holder):
            if other.tz != self.values.tz:
                raise ValueError("incompatible or non tz-aware value")
            other = other.asi8
            other_mask = isna(other)
        elif isinstance(other, (np.datetime64, datetime, date)):
            other = tslib.Timestamp(other)
            tz = getattr(other, 'tz', None)

            # test we can have an equal time zone
            if tz is None or str(tz) != str(self.values.tz):
                raise ValueError("incompatible or non tz-aware value")
            other_mask = isna(other)
            other = other.value
        else:
            raise TypeError

        return values, values_mask, other, other_mask
