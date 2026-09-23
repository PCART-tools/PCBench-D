    @Appender(generic._shared_docs['sort_index'] % _shared_doc_kwargs)
    def sort_index(self, axis=0, level=None, ascending=True, inplace=False,
                   sort_remaining=True):

        axis = self._get_axis_number(axis)
        index = self.index
        if level is not None:
            new_index, indexer = index.sortlevel(level, ascending=ascending,
                                                 sort_remaining=sort_remaining)
        elif isinstance(index, MultiIndex):
            from pandas.core.groupby import _lexsort_indexer
            indexer = _lexsort_indexer(index.labels, orders=ascending)
            indexer = _ensure_platform_int(indexer)
            new_index = index.take(indexer)
        else:
            new_index, indexer = index.sort_values(return_indexer=True,
                                                   ascending=ascending)

        new_values = self._values.take(indexer)
        result = self._constructor(new_values, index=new_index)

        if inplace:
            self._update_inplace(result)
        else:
            return result.__finalize__(self)
