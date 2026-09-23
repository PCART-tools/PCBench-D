    def to_dense(self) -> DataFrame:
        """
        Convert a DataFrame with sparse values to dense.

        .. versionadded:: 0.25.0

        Returns
        -------
        DataFrame
            A DataFrame with the same values stored as dense arrays.

        Examples
        --------
        >>> df = pd.DataFrame({"A": pd.arrays.SparseArray([0, 1, 0])})
        >>> df.sparse.to_dense()
           A
        0  0
        1  1
        2  0
        """
        from pandas import DataFrame

        data = {k: v.array.to_dense() for k, v in self._parent.items()}
        return DataFrame(data, index=self._parent.index, columns=self._parent.columns)
