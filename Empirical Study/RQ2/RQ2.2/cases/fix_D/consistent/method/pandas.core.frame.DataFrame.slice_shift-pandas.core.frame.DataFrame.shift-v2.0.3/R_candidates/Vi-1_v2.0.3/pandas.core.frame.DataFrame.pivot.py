    @Substitution("")
    @Appender(_shared_docs["pivot"])
    def pivot(self, *, columns, index=lib.NoDefault, values=lib.NoDefault) -> DataFrame:
        from pandas.core.reshape.pivot import pivot

        return pivot(self, index=index, columns=columns, values=values)
