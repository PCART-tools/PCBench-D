    def __iter__(self) -> Iterator:
        """
        Iterate over info axis.

        Returns
        -------
        iterator
            Info axis as iterator.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> for x in df:
        ...     print(x)
        A
        B
        """
        return iter(self._info_axis)
