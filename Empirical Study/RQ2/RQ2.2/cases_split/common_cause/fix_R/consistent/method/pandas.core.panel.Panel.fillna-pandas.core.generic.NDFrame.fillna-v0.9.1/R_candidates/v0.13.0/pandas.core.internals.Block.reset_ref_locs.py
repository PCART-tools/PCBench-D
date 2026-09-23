    def reset_ref_locs(self):
        """ reset the block ref_locs """
        self._ref_locs = np.empty(len(self.items), dtype='int64')
