    def _lexsort_depth(self) -> int:
        """
        Compute and return the lexsort_depth, the number of levels of the
        MultiIndex that are sorted lexically

        Returns
        ------
        int
        """
        int64_codes = [ensure_int64(level_codes) for level_codes in self.codes]
        for k in range(self.nlevels, 0, -1):
            if libalgos.is_lexsorted(int64_codes[:k]):
                return k
        return 0
