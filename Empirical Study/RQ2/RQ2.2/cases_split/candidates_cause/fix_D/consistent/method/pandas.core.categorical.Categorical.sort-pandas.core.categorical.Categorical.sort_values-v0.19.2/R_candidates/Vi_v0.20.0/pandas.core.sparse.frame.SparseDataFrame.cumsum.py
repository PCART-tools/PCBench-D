    def cumsum(self, axis=0, *args, **kwargs):
        """
        Return SparseDataFrame of cumulative sums over requested axis.

        Parameters
        ----------
        axis : {0, 1}
            0 for row-wise, 1 for column-wise

        Returns
        -------
        y : SparseDataFrame
        """
        nv.validate_cumsum(args, kwargs)

        if axis is None:
            axis = self._stat_axis_number

        return self.apply(lambda x: x.cumsum(), axis=axis)
