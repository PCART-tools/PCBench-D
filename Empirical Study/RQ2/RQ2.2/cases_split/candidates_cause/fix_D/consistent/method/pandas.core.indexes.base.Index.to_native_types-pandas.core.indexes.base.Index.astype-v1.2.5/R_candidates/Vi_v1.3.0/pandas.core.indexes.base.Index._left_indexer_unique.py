    @final
    def _left_indexer_unique(self: _IndexT, other: _IndexT) -> np.ndarray:
        # -> np.ndarray[np.intp]
        # Caller is responsible for ensuring other.dtype == self.dtype
        sv = self._get_join_target()
        ov = other._get_join_target()
        return libjoin.left_join_indexer_unique(sv, ov)
