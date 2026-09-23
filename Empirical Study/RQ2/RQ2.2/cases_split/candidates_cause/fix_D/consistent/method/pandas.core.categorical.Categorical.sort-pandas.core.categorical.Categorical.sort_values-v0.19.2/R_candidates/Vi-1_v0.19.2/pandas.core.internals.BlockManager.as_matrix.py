    def as_matrix(self, items=None):
        if len(self.blocks) == 0:
            return np.empty(self.shape, dtype=float)

        if items is not None:
            mgr = self.reindex_axis(items, axis=0)
        else:
            mgr = self

        if self._is_single_block or not self.is_mixed_type:
            return mgr.blocks[0].get_values()
        else:
            return mgr._interleave()
