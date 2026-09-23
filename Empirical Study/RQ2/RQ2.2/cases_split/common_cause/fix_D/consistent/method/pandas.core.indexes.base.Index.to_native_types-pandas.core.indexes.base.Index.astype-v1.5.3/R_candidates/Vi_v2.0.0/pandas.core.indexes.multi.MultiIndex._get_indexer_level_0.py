    def _get_indexer_level_0(self, target) -> npt.NDArray[np.intp]:
        """
        Optimized equivalent to `self.get_level_values(0).get_indexer_for(target)`.
        """
        lev = self.levels[0]
        codes = self._codes[0]
        cat = Categorical.from_codes(codes=codes, categories=lev)
        ci = Index(cat)
        return ci.get_indexer_for(target)
