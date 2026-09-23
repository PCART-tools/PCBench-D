    @Substitution(name='rolling')
    @Appender(_doc_template)
    @Appender(_shared_docs['kurt'])
    def kurt(self, **kwargs):
        return super(Rolling, self).kurt(**kwargs)
