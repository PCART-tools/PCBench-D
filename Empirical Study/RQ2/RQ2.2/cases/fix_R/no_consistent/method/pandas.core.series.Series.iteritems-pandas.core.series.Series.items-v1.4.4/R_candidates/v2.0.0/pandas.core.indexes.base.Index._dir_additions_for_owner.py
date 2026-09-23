    @final
    @cache_readonly
    def _dir_additions_for_owner(self) -> set[str_t]:
        """
        Add the string-like labels to the owner dataframe/series dir output.

        If this is a MultiIndex, it's first level values are used.
        """
        return {
            c
            for c in self.unique(level=0)[: get_option("display.max_dir_items")]
            if isinstance(c, str) and c.isidentifier()
        }
