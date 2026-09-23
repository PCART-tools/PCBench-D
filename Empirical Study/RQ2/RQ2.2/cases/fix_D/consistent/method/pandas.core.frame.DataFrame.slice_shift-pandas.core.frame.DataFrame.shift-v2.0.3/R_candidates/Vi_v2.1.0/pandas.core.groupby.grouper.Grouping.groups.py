    @cache_readonly
    def groups(self) -> dict[Hashable, np.ndarray]:
        cats = Categorical.from_codes(self.codes, self.group_index, validate=False)
        return self._index.groupby(cats)
