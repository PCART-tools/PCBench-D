    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['kurt'])
    def kurt(self, **kwargs):
        return super(Expanding, self).kurt(**kwargs)
