    def to_coo(self, row_levels=(0,), column_levels=(1,), sort_labels=False):
        """
        Create a scipy.sparse.coo_matrix from a SparseSeries with MultiIndex.

        Use row_levels and column_levels to determine the row and column
        coordinates respectively. row_levels and column_levels are the names
        (labels) or numbers of the levels. {row_levels, column_levels} must be
        a partition of the MultiIndex level names (or numbers).

        Parameters
        ----------
        row_levels : tuple/list
        column_levels : tuple/list
        sort_labels : bool, default False
            Sort the row and column labels before forming the sparse matrix.

        Returns
        -------
        y : scipy.sparse.coo_matrix
        rows : list (row labels)
        columns : list (column labels)

        Examples
        --------
        >>> s = pd.Series([3.0, np.nan, 1.0, 3.0, np.nan, np.nan])
        >>> s.index = pd.MultiIndex.from_tuples([(1, 2, 'a', 0),
                                                (1, 2, 'a', 1),
                                                (1, 1, 'b', 0),
                                                (1, 1, 'b', 1),
                                                (2, 1, 'b', 0),
                                                (2, 1, 'b', 1)],
                                                names=['A', 'B', 'C', 'D'])
        >>> ss = s.to_sparse()
        >>> A, rows, columns = ss.to_coo(row_levels=['A', 'B'],
                                         column_levels=['C', 'D'],
                                         sort_labels=True)
        >>> A
        <3x4 sparse matrix of type '<class 'numpy.float64'>'
                with 3 stored elements in COOrdinate format>
        >>> A.todense()
        matrix([[ 0.,  0.,  1.,  3.],
        [ 3.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.]])
        >>> rows
        [(1, 1), (1, 2), (2, 1)]
        >>> columns
        [('a', 0), ('a', 1), ('b', 0), ('b', 1)]
        """
        from pandas.core.sparse.scipy_sparse import _sparse_series_to_coo

        A, rows, columns = _sparse_series_to_coo(
            self._parent, row_levels, column_levels, sort_labels=sort_labels
        )
        return A, rows, columns
