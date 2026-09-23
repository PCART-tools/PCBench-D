    @cache_readonly
    def lexsort_depth(self):
        if self.sortorder is not None:
            return self.sortorder

        return self._lexsort_depth()
