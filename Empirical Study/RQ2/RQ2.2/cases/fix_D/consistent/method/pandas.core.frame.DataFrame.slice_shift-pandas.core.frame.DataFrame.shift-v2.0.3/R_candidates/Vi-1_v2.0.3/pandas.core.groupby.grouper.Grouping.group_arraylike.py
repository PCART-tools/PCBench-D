    @cache_readonly
    def group_arraylike(self) -> ArrayLike:
        """
        Analogous to result_index, but holding an ArrayLike to ensure
        we can retain ExtensionDtypes.
        """
        if self._all_grouper is not None:
            # retain dtype for categories, including unobserved ones
            return self.result_index._values

        elif self._passed_categorical:
            return self.group_index._values

        return self._codes_and_uniques[1]
