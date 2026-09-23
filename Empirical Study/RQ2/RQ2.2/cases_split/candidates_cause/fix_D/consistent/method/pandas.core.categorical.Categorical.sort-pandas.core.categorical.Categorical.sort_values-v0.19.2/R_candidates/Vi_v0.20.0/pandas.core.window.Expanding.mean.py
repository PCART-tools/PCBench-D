    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['mean'])
    def mean(self, *args, **kwargs):
        nv.validate_expanding_func('mean', args, kwargs)
        return super(Expanding, self).mean(*args, **kwargs)
