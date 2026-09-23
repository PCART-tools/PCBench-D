    def _combine(
        self, blocks: list[Block], copy: bool = True, index: Index | None = None
    ) -> Self:
        """return a new manager with the blocks"""
        if len(blocks) == 0:
            if self.ndim == 2:
                # retain our own Index dtype
                if index is not None:
                    axes = [self.items[:0], index]
                else:
                    axes = [self.items[:0]] + self.axes[1:]
                return self.make_empty(axes)
            return self.make_empty()

        # FIXME: optimization potential
        indexer = np.sort(np.concatenate([b.mgr_locs.as_array for b in blocks]))
        inv_indexer = lib.get_reverse_indexer(indexer, self.shape[0])

        new_blocks: list[Block] = []
        # TODO(CoW) we could optimize here if we know that the passed blocks
        # are fully "owned" (eg created from an operation, not coming from
        # an existing manager)
        for b in blocks:
            nb = b.copy(deep=copy)
            nb.mgr_locs = BlockPlacement(inv_indexer[nb.mgr_locs.indexer])
            new_blocks.append(nb)

        axes = list(self.axes)
        if index is not None:
            axes[-1] = index
        axes[0] = self.items.take(indexer)

        return type(self).from_blocks(new_blocks, axes)
