    @Appender(generic._shared_docs['replace'] % _shared_doc_kwargs)
    def replace(self, to_replace=None, value=None, inplace=False, limit=None,
                regex=False, method='pad'):
        return super(Series, self).replace(to_replace=to_replace, value=value,
                                           inplace=inplace, limit=limit,
                                           regex=regex, method=method)
