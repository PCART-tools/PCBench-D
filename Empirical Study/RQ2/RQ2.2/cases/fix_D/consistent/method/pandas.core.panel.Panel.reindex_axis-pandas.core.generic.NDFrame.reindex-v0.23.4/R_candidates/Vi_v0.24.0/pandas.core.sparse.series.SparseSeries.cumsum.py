    def cumsum(self, axis=0, *args, **kwargs):
        """
        Cumulative sum of non-NA/null values.

        When performing the cumulative summation, any non-NA/null values will
        be skipped. The resulting SparseSeries will preserve the locations of
        NaN values, but the fill value will be `np.nan` regardless.

        Parameters
        ----------
        axis : {0}

        Returns
        -------
        cumsum : SparseSeries
        """
        nv.validate_cumsum(args, kwargs)
        # Validate axis
        if axis is not None:
            self._get_axis_number(axis)

        new_array = self.values.cumsum()

        return self._constructor(
            new_array, index=self.index,
            sparse_index=new_array.sp_index).__finalize__(self)
