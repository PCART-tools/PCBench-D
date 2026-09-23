    @Appender(_shared_docs['reindex_axis'] % _shared_doc_kwargs)
    def reindex_axis(self, labels, axis=0, method=None, level=None, copy=True,
                     limit=None, fill_value=None):
        msg = ("'.reindex_axis' is deprecated and will be removed in a future "
               "version. Use '.reindex' instead.")
        self._consolidate_inplace()

        axis_name = self._get_axis_name(axis)
        axis_values = self._get_axis(axis_name)
        method = missing.clean_reindex_fill_method(method)
        warnings.warn(msg, FutureWarning, stacklevel=3)
        new_index, indexer = axis_values.reindex(labels, method, level,
                                                 limit=limit)
        return self._reindex_with_indexers({axis: [new_index, indexer]},
                                           fill_value=fill_value, copy=copy)
