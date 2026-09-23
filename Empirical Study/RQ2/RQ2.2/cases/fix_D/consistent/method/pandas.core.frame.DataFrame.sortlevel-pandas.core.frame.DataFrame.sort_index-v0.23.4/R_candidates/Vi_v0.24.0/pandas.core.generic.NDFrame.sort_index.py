    def sort_index(self, axis=0, level=None, ascending=True, inplace=False,
                   kind='quicksort', na_position='last', sort_remaining=True):
        """
        Sort object by labels (along an axis)

        Parameters
        ----------
        axis : %(axes)s to direct sorting
        level : int or level name or list of ints or list of level names
            if not None, sort on values in specified index level(s)
        ascending : boolean, default True
            Sort ascending vs. descending
        inplace : bool, default False
            if True, perform operation in-place
        kind : {'quicksort', 'mergesort', 'heapsort'}, default 'quicksort'
             Choice of sorting algorithm. See also ndarray.np.sort for more
             information.  `mergesort` is the only stable algorithm. For
             DataFrames, this option is only applied when sorting on a single
             column or label.
        na_position : {'first', 'last'}, default 'last'
             `first` puts NaNs at the beginning, `last` puts NaNs at the end.
             Not implemented for MultiIndex.
        sort_remaining : bool, default True
            if true and sorting by level and index is multilevel, sort by other
            levels too (in order) after sorting by specified level

        Returns
        -------
        sorted_obj : %(klass)s
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        axis = self._get_axis_number(axis)
        axis_name = self._get_axis_name(axis)
        labels = self._get_axis(axis)

        if level is not None:
            raise NotImplementedError("level is not implemented")
        if inplace:
            raise NotImplementedError("inplace is not implemented")

        sort_index = labels.argsort()
        if not ascending:
            sort_index = sort_index[::-1]

        new_axis = labels.take(sort_index)
        return self.reindex(**{axis_name: new_axis})
