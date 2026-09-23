    @final
    def ravel(self, order: str_t = "C") -> Self:
        """
        Return a view on self.

        Returns
        -------
        Index

        See Also
        --------
        numpy.ndarray.ravel : Return a flattened array.

        Examples
        --------
        >>> s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
        >>> s.index.ravel()
        Index(['a', 'b', 'c'], dtype='object')
        """
        return self[:]
