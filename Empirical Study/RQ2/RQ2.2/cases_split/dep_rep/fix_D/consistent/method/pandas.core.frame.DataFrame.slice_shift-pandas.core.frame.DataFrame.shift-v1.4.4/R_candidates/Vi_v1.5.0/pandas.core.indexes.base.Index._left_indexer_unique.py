    @final
    def _left_indexer_unique(self: _IndexT, other: _IndexT) -> npt.NDArray[np.intp]:
        # Caller is responsible for ensuring other.dtype == self.dtype
        sv = self._get_engine_target()
        ov = other._get_engine_target()
        # can_use_libjoin assures sv and ov are ndarrays
        sv = cast(np.ndarray, sv)
        ov = cast(np.ndarray, ov)
        return libjoin.left_join_indexer_unique(sv, ov)
