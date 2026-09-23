    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['quantile'])
    def quantile(self, quantile, **kwargs):
        return super(Expanding, self).quantile(quantile=quantile, **kwargs)
