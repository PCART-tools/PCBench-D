    def sortlevel(self, level=0, ascending=True, sort_remaining=True):
        """
        Sort Series with MultiIndex by chosen level. Data will be
        lexicographically sorted by the chosen level followed by the other
        levels (in order)

        Parameters
        ----------
        level : int or level name, default None
        ascending : bool, default True

        Returns
        -------
        sorted : Series
        """
        if not isinstance(self.index, MultiIndex):
            raise TypeError('can only sort by level with a hierarchical index')

        new_index, indexer = self.index.sortlevel(level, ascending=ascending,
                                                 sort_remaining=sort_remaining)
        new_values = self.values.take(indexer)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
