    @Substitution(name="expanding")
    @Appender(_doc_template)
    @Appender(_shared_docs["cov"])
    def cov(self, other=None, pairwise=None, ddof=1, **kwargs):
        return super().cov(other=other, pairwise=pairwise, ddof=ddof, **kwargs)
