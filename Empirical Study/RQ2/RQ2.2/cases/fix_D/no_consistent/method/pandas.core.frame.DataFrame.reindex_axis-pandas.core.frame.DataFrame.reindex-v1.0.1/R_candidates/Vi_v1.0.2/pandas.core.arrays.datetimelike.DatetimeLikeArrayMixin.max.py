    def max(self, axis=None, skipna=True, *args, **kwargs):
        """
        Return the maximum value of the Array or maximum along
        an axis.

        See Also
        --------
        numpy.ndarray.max
        Index.max : Return the maximum value in an Index.
        Series.max : Return the maximum value in a Series.
        """
        # TODO: skipna is broken with max.
        # See https://github.com/pandas-dev/pandas/issues/24265
        nv.validate_max(args, kwargs)
        nv.validate_minmax_axis(axis)

        mask = self.isna()
        if skipna:
            values = self[~mask].asi8
        elif mask.any():
            return NaT
        else:
            values = self.asi8

        if not len(values):
            # short-circuit for empty max / min
            return NaT

        result = nanops.nanmax(values, skipna=skipna)
        # Don't have to worry about NA `result`, since no NA went in.
        return self._box_func(result)
