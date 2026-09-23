    @cache_readonly
    def _lexsort_depth(self) -> int:
        """
        Compute and return the lexsort_depth, the number of levels of the
        MultiIndex that are sorted lexically

        Returns
        -------
        int
        """
        if self.sortorder is not None:
            return self.sortorder
        return _lexsort_depth(self.codes, self.nlevels)
