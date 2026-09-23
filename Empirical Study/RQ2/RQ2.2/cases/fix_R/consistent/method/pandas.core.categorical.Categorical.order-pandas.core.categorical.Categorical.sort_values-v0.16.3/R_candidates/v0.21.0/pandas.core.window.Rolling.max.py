    @Substitution(name='rolling')
    @Appender(_doc_template)
    @Appender(_shared_docs['max'])
    def max(self, *args, **kwargs):
        nv.validate_rolling_func('max', args, kwargs)
        return super(Rolling, self).max(*args, **kwargs)
