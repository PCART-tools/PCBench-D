    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['corr'])
    def corr(self, other=None, pairwise=None, **kwargs):
        return super(Expanding, self).corr(other=other, pairwise=pairwise,
                                           **kwargs)
