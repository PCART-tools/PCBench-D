    def to_flat_index(self) -> Index:  # type: ignore[override]
        """
        Convert a MultiIndex to an Index of Tuples containing the level values.

        Returns
        -------
        pd.Index
            Index with the MultiIndex data represented in Tuples.

        See Also
        --------
        MultiIndex.from_tuples : Convert flat index back to MultiIndex.

        Notes
        -----
        This method will simply return the caller if called by anything other
        than a MultiIndex.

        Examples
        --------
        >>> index = pd.MultiIndex.from_product(
        ...     [['foo', 'bar'], ['baz', 'qux']],
        ...     names=['a', 'b'])
        >>> index.to_flat_index()
        Index([('foo', 'baz'), ('foo', 'qux'),
               ('bar', 'baz'), ('bar', 'qux')],
              dtype='object')
        """
        return Index(self._values, tupleize_cols=False)
