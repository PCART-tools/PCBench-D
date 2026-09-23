    @final
    def _inner_indexer(
        self: _IndexT, other: _IndexT
    ) -> tuple[ArrayLike, np.ndarray, np.ndarray]:
        # Caller is responsible for ensuring other.dtype == self.dtype
        sv = self._get_join_target()
        ov = other._get_join_target()
        joined_ndarray, lidx, ridx = libjoin.inner_join_indexer(sv, ov)
        joined = self._from_join_target(joined_ndarray)
        return joined, lidx, ridx
