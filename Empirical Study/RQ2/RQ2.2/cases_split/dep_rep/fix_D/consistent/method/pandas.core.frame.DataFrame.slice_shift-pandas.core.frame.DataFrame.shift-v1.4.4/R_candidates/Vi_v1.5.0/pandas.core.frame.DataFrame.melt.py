    @Appender(_shared_docs["melt"] % {"caller": "df.melt(", "other": "melt"})
    def melt(
        self,
        id_vars=None,
        value_vars=None,
        var_name=None,
        value_name="value",
        col_level: Level = None,
        ignore_index: bool = True,
    ) -> DataFrame:

        return melt(
            self,
            id_vars=id_vars,
            value_vars=value_vars,
            var_name=var_name,
            value_name=value_name,
            col_level=col_level,
            ignore_index=ignore_index,
        ).__finalize__(self, method="melt")
