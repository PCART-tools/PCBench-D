    @Appender(_agg_doc)
    @Substitution(name='expanding')
    @Appender(_shared_docs['kurt'])
    def kurt(self, **kwargs):
        return super(Expanding, self).kurt(**kwargs)
