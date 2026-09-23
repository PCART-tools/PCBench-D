    @cache_readonly
    def groups(self) -> Dict[Hashable, np.ndarray]:
        return self.index.groupby(Categorical.from_codes(self.codes, self.group_index))
