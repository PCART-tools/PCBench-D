    def reduce(self: T, func: Callable) -> T:
        """
        Apply reduction function blockwise, returning a single-row BlockManager.

        Parameters
        ----------
        func : reduction function

        Returns
        -------
        BlockManager
        """
        # If 2D, we assume that we're operating column-wise
        assert self.ndim == 2

        res_blocks: list[Block] = []
        for blk in self.blocks:
            nbs = blk.reduce(func)
            res_blocks.extend(nbs)

        index = Index([None])  # placeholder
        new_mgr = type(self).from_blocks(res_blocks, [self.items, index])
        return new_mgr
