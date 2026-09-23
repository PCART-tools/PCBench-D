    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['skew'])
    def skew(self, **kwargs):
        return super(Expanding, self).skew(**kwargs)
