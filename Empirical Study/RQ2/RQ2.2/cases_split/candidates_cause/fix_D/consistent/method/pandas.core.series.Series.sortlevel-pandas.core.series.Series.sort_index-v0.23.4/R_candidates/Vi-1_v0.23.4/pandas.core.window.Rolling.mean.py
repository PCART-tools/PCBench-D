    @Substitution(name='rolling')
    @Appender(_shared_docs['mean'])
    def mean(self, *args, **kwargs):
        nv.validate_rolling_func('mean', args, kwargs)
        return super(Rolling, self).mean(*args, **kwargs)
