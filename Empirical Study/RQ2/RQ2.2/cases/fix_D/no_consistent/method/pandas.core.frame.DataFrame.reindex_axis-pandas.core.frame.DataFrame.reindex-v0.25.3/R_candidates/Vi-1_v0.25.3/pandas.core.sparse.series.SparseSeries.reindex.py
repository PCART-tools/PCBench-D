    @Substitution(**_shared_doc_kwargs)
    @Appender(generic.NDFrame.reindex.__doc__)
    def reindex(self, index=None, method=None, copy=True, limit=None, **kwargs):
        # TODO: remove?
        return super().reindex(
            index=index, method=method, copy=copy, limit=limit, **kwargs
        )
