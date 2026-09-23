    @Appender(generic._shared_docs['reindex'] % _shared_doc_kwargs)
    def reindex(self, index=None, method=None, copy=True, limit=None,
                **kwargs):

        return super(SparseSeries, self).reindex(index=index, method=method,
                                                 copy=copy, limit=limit,
                                                 **kwargs)
