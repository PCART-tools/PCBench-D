    @Substitution(name='expanding')
    @Appender(_shared_docs['quantile'])
    def quantile(self, quantile, interpolation='linear', **kwargs):
        return super(Expanding, self).quantile(quantile=quantile,
                                               interpolation=interpolation,
                                               **kwargs)
