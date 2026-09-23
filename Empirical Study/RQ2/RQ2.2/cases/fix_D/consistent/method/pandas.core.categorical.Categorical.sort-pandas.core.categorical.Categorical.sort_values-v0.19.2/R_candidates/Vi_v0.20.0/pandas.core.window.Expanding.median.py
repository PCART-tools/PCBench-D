    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['median'])
    def median(self, **kwargs):
        return super(Expanding, self).median(**kwargs)
