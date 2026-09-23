    @Appender(base._shared_docs['duplicated'] % _shared_doc_kwargs)
    def duplicated(self, keep='first'):
        return super(Series, self).duplicated(keep=keep)
