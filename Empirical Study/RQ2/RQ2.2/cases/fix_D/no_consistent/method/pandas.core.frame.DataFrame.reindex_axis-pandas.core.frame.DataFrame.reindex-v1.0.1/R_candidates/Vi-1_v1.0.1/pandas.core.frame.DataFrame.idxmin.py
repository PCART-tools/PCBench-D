    def idxmin(self, axis=0, skipna=True) -> Series:
        """
        Return index of first occurrence of minimum over requested axis.

        NA/null values are excluded.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to use. 0 or 'index' for row-wise, 1 or 'columns' for column-wise.
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result
            will be NA.

        Returns
        -------
        Series
            Indexes of minima along the specified axis.

        Raises
        ------
        ValueError
            * If the row/column is empty

        See Also
        --------
        Series.idxmin

        Notes
        -----
        This method is the DataFrame version of ``ndarray.argmin``.
        """
        axis = self._get_axis_number(axis)
        indices = nanops.nanargmin(self.values, axis=axis, skipna=skipna)
        index = self._get_axis(axis)
        result = [index[i] if i >= 0 else np.nan for i in indices]
        return Series(result, index=self._get_agg_axis(axis))
