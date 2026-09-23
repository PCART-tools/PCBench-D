    @Appender(_shared_docs['reindex_axis'] % _shared_doc_kwargs)
    def reindex_axis(self, labels, axis=0, method=None, level=None, copy=True,
                     limit=None, fill_value=np.nan):
        return super(Panel, self).reindex_axis(labels=labels, axis=axis,
                                               method=method, level=level,
                                               copy=copy, limit=limit,
                                               fill_value=fill_value)
