    @property
    def nlevels(self) -> int:
        """
        Integer number of levels in this MultiIndex.

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([['a'], ['b'], ['c']])
        >>> mi
        MultiIndex([('a', 'b', 'c')],
                   )
        >>> mi.nlevels
        3
        """
        return len(self._levels)
