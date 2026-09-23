    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['std'])
    def std(self, ddof=1, *args, **kwargs):
        nv.validate_expanding_func('std', args, kwargs)
        return super(Expanding, self).std(ddof=ddof, **kwargs)
