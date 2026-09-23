    @Substitution(name='rolling')
    @Appender(_shared_docs['median'])
    def median(self, **kwargs):
        return super(Rolling, self).median(**kwargs)
