    @cache_readonly
    def groups(self) -> dict[Hashable, np.ndarray]:
        return self._index.groupby(Categorical.from_codes(self.codes, self.group_index))
