    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['var'])
    def var(self, ddof=1, *args, **kwargs):
        nv.validate_expanding_func('var', args, kwargs)
        return super(Expanding, self).var(ddof=ddof, **kwargs)
