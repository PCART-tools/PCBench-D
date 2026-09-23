    def unique(self) -> Self:
        """
        Compute the ExtensionArray of unique values.

        Returns
        -------
        pandas.api.extensions.ExtensionArray

        Examples
        --------
        >>> arr = pd.array([1, 2, 3, 1, 2, 3])
        >>> arr.unique()
        <IntegerArray>
        [1, 2, 3]
        Length: 3, dtype: Int64
        """
        uniques = unique(self.astype(object))
        return self._from_sequence(uniques, dtype=self.dtype)
