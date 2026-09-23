    @cache_readonly
    def lexsort_depth(self):
        if self.sortorder is not None:
            if self.sortorder == 0:
                return self.nlevels
            else:
                return 0

        int64_codes = [ensure_int64(level_codes) for level_codes in self.codes]
        for k in range(self.nlevels, 0, -1):
            if libalgos.is_lexsorted(int64_codes[:k]):
                return k

        return 0
