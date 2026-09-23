    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['count'])
    def count(self, **kwargs):
        return super(Expanding, self).count(**kwargs)
