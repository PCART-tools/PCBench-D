    def reduce(
        self: T, func: Callable, ignore_failures: bool = False
    ) -> tuple[T, np.ndarray]:
        """
        Apply reduction function blockwise, returning a single-row BlockManager.

        Parameters
        ----------
        func : reduction function
        ignore_failures : bool, default False
            Whether to drop blocks where func raises TypeError.

        Returns
        -------
        BlockManager
        np.ndarray
            Indexer of mgr_locs that are retained.
        """
        # If 2D, we assume that we're operating column-wise
        assert self.ndim == 2

        res_blocks: list[Block] = []
        for blk in self.blocks:
            nbs = blk.reduce(func, ignore_failures)
            res_blocks.extend(nbs)

        index = Index([None])  # placeholder
        if ignore_failures:
            if res_blocks:
                indexer = np.concatenate([blk.mgr_locs.as_array for blk in res_blocks])
                new_mgr = self._combine(res_blocks, copy=False, index=index)
            else:
                indexer = []
                new_mgr = type(self).from_blocks([], [self.items[:0], index])
        else:
            indexer = np.arange(self.shape[0])
            new_mgr = type(self).from_blocks(res_blocks, [self.items, index])
        return new_mgr, indexer
