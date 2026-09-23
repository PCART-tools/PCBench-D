    @classmethod
    def from_spmatrix(cls, data, index=None, columns=None):
        """
        Create a new DataFrame from a scipy sparse matrix.

        .. versionadded:: 0.25.0

        Parameters
        ----------
        data : scipy.sparse.spmatrix
            Must be convertible to csc format.
        index, columns : Index, optional
            Row and column labels to use for the resulting DataFrame.
            Defaults to a RangeIndex.

        Returns
        -------
        DataFrame
            Each column of the DataFrame is stored as a
            :class:`SparseArray`.

        Examples
        --------
        >>> import scipy.sparse
        >>> mat = scipy.sparse.eye(3)
        >>> pd.DataFrame.sparse.from_spmatrix(mat)
             0    1    2
        0  1.0  0.0  0.0
        1  0.0  1.0  0.0
        2  0.0  0.0  1.0
        """
        from pandas import DataFrame

        data = data.tocsc()
        index, columns = cls._prep_index(data, index, columns)
        sparrays = [SparseArray.from_spmatrix(data[:, i]) for i in range(data.shape[1])]
        data = dict(enumerate(sparrays))
        result = DataFrame(data, index=index)
        result.columns = columns
        return result
