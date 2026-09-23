    @final
    def _inner_indexer(
        self: _IndexT, other: _IndexT
    ) -> tuple[ArrayLike, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
        # Caller is responsible for ensuring other.dtype == self.dtype
        sv = self._get_engine_target()
        ov = other._get_engine_target()
        # can_use_libjoin assures sv and ov are ndarrays
        sv = cast(np.ndarray, sv)
        ov = cast(np.ndarray, ov)
        joined_ndarray, lidx, ridx = libjoin.inner_join_indexer(sv, ov)
        joined = self._from_join_target(joined_ndarray)
        return joined, lidx, ridx
