    @cache_readonly
    def _dir_additions_for_owner(self) -> Set[str_t]:
        """
        Add the string-like labels to the owner dataframe/series dir output.

        If this is a MultiIndex, it's first level values are used.
        """
        return {
            c
            for c in self.unique(level=0)[:100]
            if isinstance(c, str) and c.isidentifier()
        }
