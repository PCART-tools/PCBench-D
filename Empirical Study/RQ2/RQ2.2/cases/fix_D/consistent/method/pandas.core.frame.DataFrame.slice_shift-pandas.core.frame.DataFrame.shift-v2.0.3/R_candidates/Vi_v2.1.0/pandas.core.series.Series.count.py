    def count(self):
        """
        Return number of non-NA/null observations in the Series.

        Returns
        -------
        int or Series (if level specified)
            Number of non-null values in the Series.

        See Also
        --------
        DataFrame.count : Count non-NA cells for each column or row.

        Examples
        --------
        >>> s = pd.Series([0.0, 1.0, np.nan])
        >>> s.count()
        2
        """
        return notna(self._values).sum().astype("int64")
