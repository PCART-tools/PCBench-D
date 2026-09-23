    def max(self, *, axis: int | None = None, skipna: bool = True, **kwargs):
        """
        Return the maximum value of the Array or maximum along
        an axis.

        See Also
        --------
        numpy.ndarray.max
        Index.max : Return the maximum value in an Index.
        Series.max : Return the maximum value in a Series.
        """
        nv.validate_max((), kwargs)
        nv.validate_minmax_axis(axis, self.ndim)

        if is_period_dtype(self.dtype):
            # pass datetime64 values to nanops to get correct NaT semantics
            result = nanops.nanmax(
                self._ndarray.view("M8[ns]"), axis=axis, skipna=skipna
            )
            if result is NaT:
                return result
            result = result.view("i8")
            if axis is None or self.ndim == 1:
                return self._box_func(result)
            return self._from_backing_data(result)

        result = nanops.nanmax(self._ndarray, axis=axis, skipna=skipna)
        return self._wrap_reduction_result(axis, result)
