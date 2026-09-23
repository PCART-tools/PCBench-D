    def sort(self, columns=None, column=None, axis=0, ascending=True,
             inplace=False):
        """
        Sort DataFrame either by labels (along either axis) or by the values in
        column(s)

        Parameters
        ----------
        columns : object
            Column name(s) in frame. Accepts a column name or a list or tuple
            for a nested sort.
        ascending : boolean or list, default True
            Sort ascending vs. descending. Specify list for multiple sort
            orders
        axis : {0, 1}
            Sort index/rows versus columns
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance

        Examples
        --------
        >>> result = df.sort(['A', 'B'], ascending=[1, 0])

        Returns
        -------
        sorted : DataFrame
        """
        if column is not None:  # pragma: no cover
            warnings.warn("column is deprecated, use columns", FutureWarning)
            columns = column
        return self.sort_index(by=columns, axis=axis, ascending=ascending,
                               inplace=inplace)
