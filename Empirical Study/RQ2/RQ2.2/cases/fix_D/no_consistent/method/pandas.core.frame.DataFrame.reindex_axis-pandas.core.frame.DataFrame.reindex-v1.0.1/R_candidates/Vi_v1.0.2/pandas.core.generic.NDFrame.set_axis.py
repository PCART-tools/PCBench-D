    def set_axis(self, labels, axis=0, inplace=False):
        """
        Assign desired index to given axis.

        Indexes for column or row labels can be changed by assigning
        a list-like or Index.

        .. versionchanged:: 0.21.0

           The signature is now `labels` and `axis`, consistent with
           the rest of pandas API. Previously, the `axis` and `labels`
           arguments were respectively the first and second positional
           arguments.

        Parameters
        ----------
        labels : list-like, Index
            The values for the new index.

        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to update. The value 0 identifies the rows, and 1
            identifies the columns.

        inplace : bool, default False
            Whether to return a new %(klass)s instance.

        Returns
        -------
        renamed : %(klass)s or None
            An object of same type as caller if inplace=False, None otherwise.

        See Also
        --------
        DataFrame.rename_axis : Alter the name of the index or columns.

        Examples
        --------
        **Series**

        >>> s = pd.Series([1, 2, 3])
        >>> s
        0    1
        1    2
        2    3
        dtype: int64

        >>> s.set_axis(['a', 'b', 'c'], axis=0)
        a    1
        b    2
        c    3
        dtype: int64

        **DataFrame**

        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        Change the row labels.

        >>> df.set_axis(['a', 'b', 'c'], axis='index')
           A  B
        a  1  4
        b  2  5
        c  3  6

        Change the column labels.

        >>> df.set_axis(['I', 'II'], axis='columns')
           I  II
        0  1   4
        1  2   5
        2  3   6

        Now, update the labels inplace.

        >>> df.set_axis(['i', 'ii'], axis='columns', inplace=True)
        >>> df
           i  ii
        0  1   4
        1  2   5
        2  3   6
        """
        if inplace:
            setattr(self, self._get_axis_name(axis), labels)
        else:
            obj = self.copy()
            obj.set_axis(labels, axis=axis, inplace=True)
            return obj
