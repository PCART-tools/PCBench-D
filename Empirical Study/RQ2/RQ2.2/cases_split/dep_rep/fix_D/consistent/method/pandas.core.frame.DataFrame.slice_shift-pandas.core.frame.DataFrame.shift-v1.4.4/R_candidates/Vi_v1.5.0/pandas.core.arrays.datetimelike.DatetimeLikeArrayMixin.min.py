    def min(self, *, axis: int | None = None, skipna: bool = True, **kwargs):
        """
        Return the minimum value of the Array or minimum along
        an axis.

        See Also
        --------
        numpy.ndarray.min
        Index.min : Return the minimum value in an Index.
        Series.min : Return the minimum value in a Series.
        """
        nv.validate_min((), kwargs)
        nv.validate_minmax_axis(axis, self.ndim)

        if is_period_dtype(self.dtype):
            # pass datetime64 values to nanops to get correct NaT semantics
            result = nanops.nanmin(
                self._ndarray.view("M8[ns]"), axis=axis, skipna=skipna
            )
            if result is NaT:
                return NaT
            result = result.view("i8")
            if axis is None or self.ndim == 1:
                return self._box_func(result)
            return self._from_backing_data(result)

        result = nanops.nanmin(self._ndarray, axis=axis, skipna=skipna)
        return self._wrap_reduction_result(axis, result)
