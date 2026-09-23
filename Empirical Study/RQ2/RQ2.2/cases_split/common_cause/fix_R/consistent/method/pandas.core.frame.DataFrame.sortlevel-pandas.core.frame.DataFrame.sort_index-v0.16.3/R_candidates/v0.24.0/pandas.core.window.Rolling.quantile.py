    @Substitution(name='rolling')
    @Appender(_shared_docs['quantile'])
    def quantile(self, quantile, interpolation='linear', **kwargs):
        return super(Rolling, self).quantile(quantile=quantile,
                                             interpolation=interpolation,
                                             **kwargs)
