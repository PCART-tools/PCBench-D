    def take_ref_locs(self, indexer):
        """
        need to preserve the ref_locs and just shift them
        return None if ref_locs is None

        see GH6509
        """

        ref_locs = self._ref_locs
        if ref_locs is None:
            return None

        tindexer = np.ones(len(ref_locs),dtype=bool)
        tindexer[indexer] = False
        tindexer = tindexer.astype(int).cumsum()[indexer]
        ref_locs = ref_locs[indexer]
        ref_locs -= tindexer
        return ref_locs
