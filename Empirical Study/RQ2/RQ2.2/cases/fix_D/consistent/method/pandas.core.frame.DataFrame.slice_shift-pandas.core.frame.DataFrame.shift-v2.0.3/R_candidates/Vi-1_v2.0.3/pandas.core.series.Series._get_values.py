    def _get_values(self, indexer: slice | npt.NDArray[np.bool_]) -> Series:
        new_mgr = self._mgr.getitem_mgr(indexer)
        return self._constructor(new_mgr).__finalize__(self)
