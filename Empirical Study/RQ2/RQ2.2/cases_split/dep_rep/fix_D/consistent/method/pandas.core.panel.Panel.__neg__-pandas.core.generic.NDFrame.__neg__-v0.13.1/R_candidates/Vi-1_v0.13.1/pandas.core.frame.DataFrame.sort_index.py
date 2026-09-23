    def sort_index(self, axis=0, by=None, ascending=True, inplace=False,
                   kind='quicksort'):
        """
        Sort DataFrame either by labels (along either axis) or by the values in
        a column

        Parameters
        ----------
        axis : {0, 1}
            Sort index/rows versus columns
        by : object
            Column name(s) in frame. Accepts a column name or a list or tuple
            for a nested sort.
        ascending : boolean or list, default True
            Sort ascending vs. descending. Specify list for multiple sort
            orders
        inplace : boolean, default False
            Sort the DataFrame without creating a new instance

        Examples
        --------
        >>> result = df.sort_index(by=['A', 'B'], ascending=[True, False])

        Returns
        -------
        sorted : DataFrame
        """
        from pandas.core.groupby import _lexsort_indexer

        axis = self._get_axis_number(axis)
        if axis not in [0, 1]:  # pragma: no cover
            raise AssertionError('Axis must be 0 or 1, got %s' % str(axis))

        labels = self._get_axis(axis)

        if by is not None:
            if axis != 0:
                raise ValueError('When sorting by column, axis must be 0 '
                                 '(rows)')
            if not isinstance(by, (tuple, list)):
                by = [by]
            if com._is_sequence(ascending) and len(by) != len(ascending):
                raise ValueError('Length of ascending (%d) != length of by'
                                 ' (%d)' % (len(ascending), len(by)))

            if len(by) > 1:
                keys = []
                for x in by:
                    k = self[x].values
                    if k.ndim == 2:
                        raise ValueError('Cannot sort by duplicate column %s'
                                         % str(x))
                    keys.append(k)

                def trans(v):
                    if com.needs_i8_conversion(v):
                        return v.view('i8')
                    return v

                keys = [trans(self[x].values) for x in by]
                indexer = _lexsort_indexer(keys, orders=ascending)
                indexer = com._ensure_platform_int(indexer)
            else:
                by = by[0]
                k = self[by].values
                if k.ndim == 2:
                    raise ValueError('Cannot sort by duplicate column %s'
                                     % str(by))
                indexer = k.argsort(kind=kind)
                if isinstance(ascending, (tuple, list)):
                    ascending = ascending[0]
                if not ascending:
                    indexer = indexer[::-1]
        elif isinstance(labels, MultiIndex):
            indexer = _lexsort_indexer(labels.labels, orders=ascending)
            indexer = com._ensure_platform_int(indexer)
        else:
            indexer = labels.argsort(kind=kind)
            if not ascending:
                indexer = indexer[::-1]

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
