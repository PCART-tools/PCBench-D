    def __init__(
        self, bins, binlabels, filter_empty=False, mutated=False, indexer=None
    ):
        self.bins = ensure_int64(bins)
        self.binlabels = ensure_index(binlabels)
        self._filter_empty_groups = filter_empty
        self.mutated = mutated
        self.indexer = indexer
