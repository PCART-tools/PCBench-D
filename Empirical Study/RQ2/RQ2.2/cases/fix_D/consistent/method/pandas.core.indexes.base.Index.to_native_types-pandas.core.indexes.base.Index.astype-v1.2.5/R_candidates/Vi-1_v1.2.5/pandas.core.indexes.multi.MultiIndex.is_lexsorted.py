    def is_lexsorted(self) -> bool:
        """
        Return True if the codes are lexicographically sorted.

        Returns
        -------
        bool

        Examples
        --------
        In the below examples, the first level of the MultiIndex is sorted because
        a<b<c, so there is no need to look at the next level.

        >>> pd.MultiIndex.from_arrays([['a', 'b', 'c'], ['d', 'e', 'f']]).is_lexsorted()
        True
        >>> pd.MultiIndex.from_arrays([['a', 'b', 'c'], ['d', 'f', 'e']]).is_lexsorted()
        True

        In case there is a tie, the lexicographical sorting looks
        at the next level of the MultiIndex.

        >>> pd.MultiIndex.from_arrays([[0, 1, 1], ['a', 'b', 'c']]).is_lexsorted()
        True
        >>> pd.MultiIndex.from_arrays([[0, 1, 1], ['a', 'c', 'b']]).is_lexsorted()
        False
        >>> pd.MultiIndex.from_arrays([['a', 'a', 'b', 'b'],
        ...                            ['aa', 'bb', 'aa', 'bb']]).is_lexsorted()
        True
        >>> pd.MultiIndex.from_arrays([['a', 'a', 'b', 'b'],
        ...                            ['bb', 'aa', 'aa', 'bb']]).is_lexsorted()
        False
        """
        return self.lexsort_depth == self.nlevels
