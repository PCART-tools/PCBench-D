    @Substitution(name='rolling')
    @Appender(_doc_template)
    @Appender(_shared_docs['quantile'])
    def quantile(self, quantile, **kwargs):
        return super(Rolling, self).quantile(quantile=quantile, **kwargs)
