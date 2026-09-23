    @Substitution(name='expanding')
    @Appender(_shared_docs['count'])
    def count(self, **kwargs):
        return super(Expanding, self).count(**kwargs)
