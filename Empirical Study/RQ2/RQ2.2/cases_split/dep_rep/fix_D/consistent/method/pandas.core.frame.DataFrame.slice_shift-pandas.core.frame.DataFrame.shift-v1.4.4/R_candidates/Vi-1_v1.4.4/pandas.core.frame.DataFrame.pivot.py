    @Substitution("")
    @Appender(_shared_docs["pivot"])
    def pivot(self, index=None, columns=None, values=None) -> DataFrame:
        from pandas.core.reshape.pivot import pivot

        return pivot(self, index=index, columns=columns, values=values)
