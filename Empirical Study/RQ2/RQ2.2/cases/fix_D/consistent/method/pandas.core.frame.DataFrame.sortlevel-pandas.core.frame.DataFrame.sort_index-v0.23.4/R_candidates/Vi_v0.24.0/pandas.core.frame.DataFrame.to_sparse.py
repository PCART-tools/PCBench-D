    def to_sparse(self, fill_value=None, kind='block'):
        """
        Convert to SparseDataFrame.

        Implement the sparse version of the DataFrame meaning that any data
        matching a specific value it's omitted in the representation.
        The sparse DataFrame allows for a more efficient storage.

        Parameters
        ----------
        fill_value : float, default None
            The specific value that should be omitted in the representation.
        kind : {'block', 'integer'}, default 'block'
            The kind of the SparseIndex tracking where data is not equal to
            the fill value:

            - 'block' tracks only the locations and sizes of blocks of data.
            - 'integer' keeps an array with all the locations of the data.

            In most cases 'block' is recommended, since it's more memory
            efficient.

        Returns
        -------
        SparseDataFrame
            The sparse representation of the DataFrame.

        See Also
        --------
        DataFrame.to_dense :
            Converts the DataFrame back to the its dense form.

        Examples
        --------
        >>> df = pd.DataFrame([(np.nan, np.nan),
        ...                    (1., np.nan),
        ...                    (np.nan, 1.)])
        >>> df
             0    1
        0  NaN  NaN
        1  1.0  NaN
        2  NaN  1.0
        >>> type(df)
        <class 'pandas.core.frame.DataFrame'>

        >>> sdf = df.to_sparse()
        >>> sdf
             0    1
        0  NaN  NaN
        1  1.0  NaN
        2  NaN  1.0
        >>> type(sdf)
        <class 'pandas.core.sparse.frame.SparseDataFrame'>
        """
        from pandas.core.sparse.api import SparseDataFrame
        return SparseDataFrame(self._series, index=self.index,
                               columns=self.columns, default_kind=kind,
                               default_fill_value=fill_value)
