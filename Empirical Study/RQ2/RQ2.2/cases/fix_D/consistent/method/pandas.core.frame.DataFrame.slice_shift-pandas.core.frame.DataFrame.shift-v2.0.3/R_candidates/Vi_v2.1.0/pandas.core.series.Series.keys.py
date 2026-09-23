    def keys(self) -> Index:
        """
        Return alias for index.

        Returns
        -------
        Index
            Index of the Series.

        Examples
        --------
        >>> s = pd.Series([1, 2, 3], index=[0, 1, 2])
        >>> s.keys()
        Index([0, 1, 2], dtype='int64')
        """
        return self.index
