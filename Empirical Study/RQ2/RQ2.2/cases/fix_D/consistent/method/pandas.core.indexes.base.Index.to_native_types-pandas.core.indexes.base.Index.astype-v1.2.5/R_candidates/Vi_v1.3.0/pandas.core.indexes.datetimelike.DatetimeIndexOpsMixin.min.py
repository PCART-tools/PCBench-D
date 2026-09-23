    def min(self, axis=None, skipna=True, *args, **kwargs):
        """
        Return the minimum value of the Index or minimum along
        an axis.

        See Also
        --------
        numpy.ndarray.min
        Series.min : Return the minimum value in a Series.
        """
        nv.validate_min(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not len(self):
            return self._na_value

        i8 = self.asi8

        if len(i8) and self.is_monotonic_increasing:
            # quick check
            if i8[0] != iNaT:
                return self._data._box_func(i8[0])

        if self.hasnans:
            if not skipna:
                return self._na_value
            i8 = i8[~self._isnan]

        if not len(i8):
            return self._na_value

        min_stamp = i8.min()
        return self._data._box_func(min_stamp)
