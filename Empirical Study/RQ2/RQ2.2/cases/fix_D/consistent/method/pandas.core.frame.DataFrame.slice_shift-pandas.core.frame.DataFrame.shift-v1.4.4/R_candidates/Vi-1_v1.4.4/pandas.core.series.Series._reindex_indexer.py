    def _reindex_indexer(
        self, new_index: Index | None, indexer: npt.NDArray[np.intp] | None, copy: bool
    ) -> Series:
        # Note: new_index is None iff indexer is None
        # if not None, indexer is np.intp
        if indexer is None:
            if copy:
                return self.copy()
            return self

        new_values = algorithms.take_nd(
            self._values, indexer, allow_fill=True, fill_value=None
        )
        return self._constructor(new_values, index=new_index)
