    def delete(self, item):
        """
        Delete selected item (items if non-unique) in-place.
        """
        indexer = self.items.get_loc(item)

        is_deleted = np.zeros(self.shape[0], dtype=np.bool_)
        is_deleted[indexer] = True
        ref_loc_offset = -is_deleted.cumsum()

        is_blk_deleted = [False] * len(self.blocks)

        if isinstance(indexer, int):
            affected_start = indexer
        else:
            affected_start = is_deleted.nonzero()[0][0]

        for blkno, _ in _fast_count_smallints(self._blknos[affected_start:]):
            blk = self.blocks[blkno]
            bml = blk.mgr_locs
            blk_del = is_deleted[bml.indexer].nonzero()[0]

            if len(blk_del) == len(bml):
                is_blk_deleted[blkno] = True
                continue
            elif len(blk_del) != 0:
                blk.delete(blk_del)
                bml = blk.mgr_locs

            blk.mgr_locs = bml.add(ref_loc_offset[bml.indexer])

        # FIXME: use Index.delete as soon as it uses fastpath=True
        self.axes[0] = self.items[~is_deleted]
        self.blocks = tuple(
            b for blkno, b in enumerate(self.blocks) if not is_blk_deleted[blkno]
        )
        self._shape = None
        self._rebuild_blknos_and_blklocs()
