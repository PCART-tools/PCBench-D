    @cache_readonly
    def _inferred_type_levels(self) -> list[str]:
        """return a list of the inferred types, one for each level"""
        return [i.inferred_type for i in self.levels]
