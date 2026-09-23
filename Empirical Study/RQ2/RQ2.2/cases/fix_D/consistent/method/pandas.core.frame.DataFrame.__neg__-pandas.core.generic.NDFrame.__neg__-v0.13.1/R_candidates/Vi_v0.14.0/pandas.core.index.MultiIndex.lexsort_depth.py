    @cache_readonly
    def lexsort_depth(self):
        if self.sortorder is not None:
            if self.sortorder == 0:
                return self.nlevels
            else:
                return 0

        int64_labels = [com._ensure_int64(lab) for lab in self.labels]
        for k in range(self.nlevels, 0, -1):
            if lib.is_lexsorted(int64_labels[:k]):
                return k

        return 0
