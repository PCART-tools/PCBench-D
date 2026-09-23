    @Substitution(name='rolling')
    @Appender(_doc_template)
    @Appender(_shared_docs['corr'])
    def corr(self, other=None, pairwise=None, **kwargs):
        return super(Rolling, self).corr(other=other, pairwise=pairwise,
                                         **kwargs)
