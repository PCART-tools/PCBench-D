    def _iset_split_block(
        self,
        blkno_l: int,
        blk_locs: np.ndarray | list[int],
        value: ArrayLike | None = None,
    ) -> None:
        """Removes columns from a block by splitting the block.

        Avoids copying the whole block through slicing and updates the manager
        after determinint the new block structure. Optionally adds a new block,
        otherwise has to be done by the caller.

        Parameters
        ----------
        blkno_l: The block number to operate on, relevant for updating the manager
        blk_locs: The locations of our block that should be deleted.
        value: The value to set as a replacement.
        """
        blk = self.blocks[blkno_l]

        if self._blklocs is None:
            self._rebuild_blknos_and_blklocs()

        nbs_tup = tuple(blk.delete(blk_locs))
        if value is not None:
            locs = blk.mgr_locs.as_array[blk_locs]
            first_nb = new_block_2d(value, BlockPlacement(locs))
        else:
            first_nb = nbs_tup[0]
            nbs_tup = tuple(nbs_tup[1:])

        nr_blocks = len(self.blocks)
        blocks_tup = (
            self.blocks[:blkno_l] + (first_nb,) + self.blocks[blkno_l + 1 :] + nbs_tup
        )
        self.blocks = blocks_tup

        if not nbs_tup and value is not None:
            # No need to update anything if split did not happen
            return

        self._blklocs[first_nb.mgr_locs.indexer] = np.arange(len(first_nb))

        for i, nb in enumerate(nbs_tup):
            self._blklocs[nb.mgr_locs.indexer] = np.arange(len(nb))
            self._blknos[nb.mgr_locs.indexer] = i + nr_blocks
