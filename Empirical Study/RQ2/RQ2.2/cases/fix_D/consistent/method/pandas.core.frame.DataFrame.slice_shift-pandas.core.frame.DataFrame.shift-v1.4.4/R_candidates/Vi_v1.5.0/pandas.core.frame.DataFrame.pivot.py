    @Substitution("")
    @Appender(_shared_docs["pivot"])
    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def pivot(self, index=None, columns=None, values=None) -> DataFrame:
        from pandas.core.reshape.pivot import pivot

        return pivot(self, index=index, columns=columns, values=values)
