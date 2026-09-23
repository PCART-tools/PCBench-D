    def sort(self, columns=None, axis=0, ascending=True,
             inplace=False, kind='quicksort', na_position='last'):
        """
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
        axis : {0, 1}
            Sort index/rows versus columns
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance
        kind : {'quicksort', 'mergesort', 'heapsort'}, optional
            This option is only applied when sorting on a single column or label.
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
        return self.sort_index(by=columns, axis=axis, ascending=ascending,
                               inplace=inplace, kind=kind, na_position=na_position)
