    @Substitution("")
    @Appender(_shared_docs["pivot"])
    def pivot(
        self, *, columns, index=lib.no_default, values=lib.no_default
    ) -> DataFrame:
        from pandas.core.reshape.pivot import pivot

        return pivot(self, index=index, columns=columns, values=values)
