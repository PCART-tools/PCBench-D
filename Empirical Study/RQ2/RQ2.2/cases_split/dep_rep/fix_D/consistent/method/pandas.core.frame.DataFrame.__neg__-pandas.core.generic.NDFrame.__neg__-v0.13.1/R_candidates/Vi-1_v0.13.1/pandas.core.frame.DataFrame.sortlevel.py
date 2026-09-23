    def sortlevel(self, level=0, axis=0, ascending=True, inplace=False):
        """
        Sort multilevel index by chosen axis and primary level. Data will be
        lexicographically sorted by the chosen level followed by the other
        levels (in order)

        Parameters
        ----------
        level : int
        axis : {0, 1}
        ascending : boolean, default True
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance

        Returns
        -------
        sorted : DataFrame
        """
        axis = self._get_axis_number(axis)
        the_axis = self._get_axis(axis)
        if not isinstance(the_axis, MultiIndex):
            raise TypeError('can only sort by level with a hierarchical index')

        new_axis, indexer = the_axis.sortlevel(level, ascending=ascending)

        if self._is_mixed_type and not inplace:
            ax = 'index' if axis == 0 else 'columns'

            if new_axis.is_unique:
                d = {ax: new_axis}
            else:
                d = {ax: indexer, 'takeable': True}
            return self.reindex(**d)

        if inplace:
            if axis == 1:
                new_data = self._data.reindex_items(
                    self._data.items[indexer],
                    copy=False)
            elif axis == 0:
                new_data = self._data.take(indexer)
            self._update_inplace(new_data)
        else:
            return self.take(indexer, axis=axis, convert=False, is_copy=False)
