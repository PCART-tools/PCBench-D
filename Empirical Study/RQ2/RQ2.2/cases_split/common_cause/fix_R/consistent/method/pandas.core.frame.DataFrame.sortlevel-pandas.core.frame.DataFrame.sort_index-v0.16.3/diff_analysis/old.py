    def sortlevel(self, level=0, axis=0, ascending=True,
                  inplace=False, sort_remaining=True):
        """
        Sort multilevel index by chosen axis and primary level. Data will be
        lexicographically sorted by the chosen level followed by the other
        levels (in order)

        Parameters
        ----------
        level : int
        axis : {0 or 'index', 1 or 'columns'}, default 0
        ascending : boolean, default True
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance
        sort_remaining : boolean, default True
            Sort by the other levels too.

        Returns
        -------
        sorted : DataFrame
        """
        axis = self._get_axis_number(axis)
        the_axis = self._get_axis(axis)
        if not isinstance(the_axis, MultiIndex):
            raise TypeError('can only sort by level with a hierarchical index')

        new_axis, indexer = the_axis.sortlevel(level, ascending=ascending,
                                               sort_remaining=sort_remaining)

        if self._is_mixed_type and not inplace:
            ax = 'index' if axis == 0 else 'columns'

            if new_axis.is_unique:
                return self.reindex(**{ax: new_axis})
            else:
                return self.take(indexer, axis=axis, convert=False)

        bm_axis = self._get_block_manager_axis(axis)
        new_data = self._data.take(indexer, axis=bm_axis,
                                   convert=False, verify=False)
        if inplace:
            return self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
