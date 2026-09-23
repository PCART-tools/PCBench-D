    def sort_index(self, axis=0, by=None, ascending=True, inplace=False,
                   kind='quicksort', na_position='last'):
        """
        Sort DataFrame either by labels (along either axis) or by the values in
        a column

        Parameters
        ----------
        axis : {0, 1}
            Sort index/rows versus columns
        by : object
            Column name(s) in frame. Accepts a column name or a list
            for a nested sort. A tuple will be interpreted as the
            levels of a multi-index.
        ascending : boolean or list, default True
            Sort ascending vs. descending. Specify list for multiple sort
            orders
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance
        na_position : {'first', 'last'} (optional, default='last')
            'first' puts NaNs at the beginning
            'last' puts NaNs at the end
        kind : {'quicksort', 'mergesort', 'heapsort'}, optional
            This option is only applied when sorting on a single column or label.

        Examples
        --------
        >>> result = df.sort_index(by=['A', 'B'], ascending=[True, False])

        Returns
        -------
        sorted : DataFrame
        """

        from pandas.core.groupby import _lexsort_indexer, _nargsort
        axis = self._get_axis_number(axis)
        if axis not in [0, 1]:  # pragma: no cover
            raise AssertionError('Axis must be 0 or 1, got %s' % str(axis))

        labels = self._get_axis(axis)

        if by is not None:
            if axis != 0:
                raise ValueError('When sorting by column, axis must be 0 '
                                 '(rows)')
            if not isinstance(by, list):
                by = [by]
            if com._is_sequence(ascending) and len(by) != len(ascending):
                raise ValueError('Length of ascending (%d) != length of by'
                                 ' (%d)' % (len(ascending), len(by)))
            if len(by) > 1:
                def trans(v):
                    if com.needs_i8_conversion(v):
                        return v.view('i8')
                    return v
                keys = []
                for x in by:
                    k = self[x].values
                    if k.ndim == 2:
                        raise ValueError('Cannot sort by duplicate column %s' % str(x))
                    keys.append(trans(k))
                indexer = _lexsort_indexer(keys, orders=ascending,
                                           na_position=na_position)
                indexer = com._ensure_platform_int(indexer)
            else:
                by = by[0]
                k = self[by].values
                if k.ndim == 2:

                    # try to be helpful
                    if isinstance(self.columns, MultiIndex):
                        raise ValueError('Cannot sort by column %s in a multi-index'
                                         '  you need to explicity provide all the levels'
                                         % str(by))

                    raise ValueError('Cannot sort by duplicate column %s'
                                     % str(by))
                if isinstance(ascending, (tuple, list)):
                    ascending = ascending[0]

                indexer = _nargsort(k, kind=kind, ascending=ascending,
                                    na_position=na_position)

        elif isinstance(labels, MultiIndex):

            # make sure that the axis is lexsorted to start
            # if not we need to reconstruct to get the correct indexer
            if not labels.is_lexsorted():
                labels = MultiIndex.from_tuples(labels.values)

            indexer = _lexsort_indexer(labels.labels, orders=ascending,
                                       na_position=na_position)
            indexer = com._ensure_platform_int(indexer)
        else:
            indexer = _nargsort(labels, kind=kind, ascending=ascending,
                                na_position=na_position)

        bm_axis = self._get_block_manager_axis(axis)
        new_data = self._data.take(indexer, axis=bm_axis,
                                   convert=False, verify=False)

        if inplace:
            return self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
