    @cache_readonly
    def group_index(self) -> Index:
        if self._group_index is not None:
            # _group_index is set in __init__ for MultiIndex cases
            return self._group_index

        uniques = self._codes_and_uniques[1]
        return Index._with_infer(uniques, name=self.name)
