    @deprecate_kwarg('take_last', 'keep', mapping={True: 'last',
                                                   False: 'first'})
    @Appender(base._shared_docs['duplicated'] % _shared_doc_kwargs)
    def duplicated(self, keep='first'):
        return super(Series, self).duplicated(keep=keep)
