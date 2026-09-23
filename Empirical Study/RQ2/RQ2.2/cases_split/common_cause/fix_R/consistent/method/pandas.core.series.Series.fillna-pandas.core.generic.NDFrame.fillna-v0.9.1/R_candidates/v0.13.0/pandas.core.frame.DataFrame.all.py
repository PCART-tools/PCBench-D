    def all(self, axis=None, bool_only=None, skipna=True, level=None,
            **kwargs):
        """
        Return whether all elements are True over requested axis.
        %(na_action)s

        Parameters
        ----------
        axis : {0, 1}
            0 for row-wise, 1 for column-wise
        skipna : boolean, default True
            Exclude NA/null values. If an entire row/column is NA, the result
            will be NA
        level : int, default None
            If the axis is a MultiIndex (hierarchical), count along a
            particular level, collapsing into a DataFrame
        bool_only : boolean, default None
            Only include boolean data.

        Returns
        -------
        any : Series (or DataFrame if level specified)
        """
        if axis is None:
            axis = self._stat_axis_number
        if level is not None:
            return self._agg_by_level('all', axis=axis, level=level,
                                      skipna=skipna)
        return self._reduce(nanops.nanall, axis=axis, skipna=skipna,
                            numeric_only=bool_only, filter_type='bool')
