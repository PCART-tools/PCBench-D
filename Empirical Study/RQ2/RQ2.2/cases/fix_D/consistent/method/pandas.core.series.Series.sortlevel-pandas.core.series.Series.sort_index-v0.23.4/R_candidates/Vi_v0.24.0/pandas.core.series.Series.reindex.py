    @Substitution(**_shared_doc_kwargs)
    @Appender(generic.NDFrame.reindex.__doc__)
    def reindex(self, index=None, **kwargs):
        return super(Series, self).reindex(index=index, **kwargs)
