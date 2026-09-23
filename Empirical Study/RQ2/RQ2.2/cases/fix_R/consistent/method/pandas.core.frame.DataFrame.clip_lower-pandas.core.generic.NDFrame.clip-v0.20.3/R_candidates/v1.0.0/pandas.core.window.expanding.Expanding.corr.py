    @Substitution(name="expanding")
    @Appender(_shared_docs["corr"])
    def corr(self, other=None, pairwise=None, **kwargs):
        return super().corr(other=other, pairwise=pairwise, **kwargs)
