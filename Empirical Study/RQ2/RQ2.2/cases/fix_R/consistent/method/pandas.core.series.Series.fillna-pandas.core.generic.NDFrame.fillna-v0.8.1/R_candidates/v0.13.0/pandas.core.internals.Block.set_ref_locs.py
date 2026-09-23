    def set_ref_locs(self, placement):
        """ explicity set the ref_locs indexer, only necessary for duplicate
        indicies
        """
        if placement is None:
            self._ref_locs = None
        else:
            self._ref_locs = np.array(placement, dtype='int64', copy=True)
