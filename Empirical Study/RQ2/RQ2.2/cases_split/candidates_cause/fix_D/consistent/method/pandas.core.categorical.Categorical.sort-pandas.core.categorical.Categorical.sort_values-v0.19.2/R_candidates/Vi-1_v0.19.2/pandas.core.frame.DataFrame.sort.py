    def sort(self, columns=None, axis=0, ascending=True, inplace=False,
             kind='quicksort', na_position='last', **kwargs):
        """
        DEPRECATED: use :meth:`DataFrame.sort_values`

        Sort DataFrame either by labels (along either axis) or by the values in
        column(s)

        Parameters
        ----------
        columns : object
            Column name(s) in frame. Accepts a column name or a list
            for a nested sort. A tuple will be interpreted as the
            levels of a multi-index.
        ascending : boolean or list, default True
            Sort ascending vs. descending. Specify list for multiple sort
            orders
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Sort index/rows versus columns
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance
        kind : {'quicksort', 'mergesort', 'heapsort'}, optional
            This option is only applied when sorting on a single column or
            label.
        na_position : {'first', 'last'} (optional, default='last')
            'first' puts NaNs at the beginning
            'last' puts NaNs at the end

        Examples
        --------
        >>> result = df.sort(['A', 'B'], ascending=[1, 0])

        Returns
        -------
        sorted : DataFrame
        """
        nv.validate_sort(tuple(), kwargs)

        if columns is None:
            warnings.warn("sort(....) is deprecated, use sort_index(.....)",
                          FutureWarning, stacklevel=2)
            return self.sort_index(axis=axis, ascending=ascending,
                                   inplace=inplace)

        warnings.warn("sort(columns=....) is deprecated, use "
                      "sort_values(by=.....)", FutureWarning, stacklevel=2)
        return self.sort_values(by=columns, axis=axis, ascending=ascending,
                                inplace=inplace, kind=kind,
                                na_position=na_position)
