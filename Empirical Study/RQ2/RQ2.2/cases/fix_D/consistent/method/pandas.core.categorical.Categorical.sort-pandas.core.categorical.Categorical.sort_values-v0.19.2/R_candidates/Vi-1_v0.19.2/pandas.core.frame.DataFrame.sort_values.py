    @Appender(_shared_docs['sort_values'] % _shared_doc_kwargs)
    def sort_values(self, by, axis=0, ascending=True, inplace=False,
                    kind='quicksort', na_position='last'):

        axis = self._get_axis_number(axis)
        other_axis = 0 if axis == 1 else 1

        if not isinstance(by, list):
            by = [by]
        if is_sequence(ascending) and len(by) != len(ascending):
            raise ValueError('Length of ascending (%d) != length of by (%d)' %
                             (len(ascending), len(by)))
        if len(by) > 1:
            from pandas.core.groupby import _lexsort_indexer

            def trans(v):
                if needs_i8_conversion(v):
                    return v.view('i8')
                return v

            keys = []
            for x in by:
                k = self.xs(x, axis=other_axis).values
                if k.ndim == 2:
                    raise ValueError('Cannot sort by duplicate column %s' %
                                     str(x))
                keys.append(trans(k))
            indexer = _lexsort_indexer(keys, orders=ascending,
                                       na_position=na_position)
            indexer = _ensure_platform_int(indexer)
        else:
            from pandas.core.groupby import _nargsort

            by = by[0]
            k = self.xs(by, axis=other_axis).values
            if k.ndim == 2:

                # try to be helpful
                if isinstance(self.columns, MultiIndex):
                    raise ValueError('Cannot sort by column %s in a '
                                     'multi-index you need to explicity '
                                     'provide all the levels' % str(by))

                raise ValueError('Cannot sort by duplicate column %s' %
                                 str(by))
            if isinstance(ascending, (tuple, list)):
                ascending = ascending[0]

            indexer = _nargsort(k, kind=kind, ascending=ascending,
                                na_position=na_position)

        new_data = self._data.take(indexer,
                                   axis=self._get_block_manager_axis(axis),
                                   convert=False, verify=False)

        if inplace:
            return self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
