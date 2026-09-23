    @Appender(_shared_docs['reindex_axis'] % _shared_doc_kwargs)
    def reindex_axis(self, labels, axis=0, method=None, level=None, copy=True,
                     limit=None, fill_value=np.nan):
        self._consolidate_inplace()

        axis_name = self._get_axis_name(axis)
        axis_values = self._get_axis(axis_name)
        method = com._clean_fill_method(method)
        new_index, indexer = axis_values.reindex(
            labels, method, level, limit=limit, copy_if_needed=True)
        return self._reindex_with_indexers(
            {axis: [new_index, indexer]}, method=method, fill_value=fill_value,
            limit=limit, copy=copy)
