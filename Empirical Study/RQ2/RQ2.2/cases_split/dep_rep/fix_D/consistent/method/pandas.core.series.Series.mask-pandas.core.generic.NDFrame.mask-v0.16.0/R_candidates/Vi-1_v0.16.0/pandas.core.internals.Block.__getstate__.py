    def __getstate__(self):
        return self.mgr_locs.indexer, self.values
