    @Appender(base._shared_docs['duplicated'] % _shared_doc_kwargs)
    def duplicated(self, take_last=False):
        return super(Series, self).duplicated(take_last=take_last)
