    def max(self, axis=None, skipna=True, *args, **kwargs):
        """
        Return the maximum value of the Index or maximum along
        an axis.

        See Also
        --------
        numpy.ndarray.max
        Series.max : Return the maximum value in a Series.
        """
        nv.validate_max(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not len(self):
            return self._na_value

        i8 = self.asi8

        if len(i8) and self.is_monotonic:
            # quick check
            if i8[-1] != iNaT:
                return self._data._box_func(i8[-1])

        if self.hasnans:
            if not skipna:
                return self._na_value
            i8 = i8[~self._isnan]

        if not len(i8):
            return self._na_value

        max_stamp = i8.max()
        return self._data._box_func(max_stamp)
