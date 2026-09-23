    @cache_readonly
    def sort_idx(self):
        # Counting sort indexer
        return _algos.groupsort_indexer(self.labels, self.ngroups)[0]
