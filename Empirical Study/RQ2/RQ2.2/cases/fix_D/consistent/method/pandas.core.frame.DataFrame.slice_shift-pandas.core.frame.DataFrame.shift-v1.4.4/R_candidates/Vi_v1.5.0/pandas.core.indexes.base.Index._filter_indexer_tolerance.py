    @final
    def _filter_indexer_tolerance(
        self,
        target: Index,
        indexer: npt.NDArray[np.intp],
        tolerance,
    ) -> npt.NDArray[np.intp]:

        distance = self._difference_compat(target, indexer)

        return np.where(distance <= tolerance, indexer, -1)
