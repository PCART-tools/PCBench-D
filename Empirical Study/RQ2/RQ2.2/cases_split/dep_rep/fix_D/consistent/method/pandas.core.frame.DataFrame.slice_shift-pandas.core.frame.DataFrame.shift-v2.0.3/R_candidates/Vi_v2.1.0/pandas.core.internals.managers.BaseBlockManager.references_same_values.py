    def references_same_values(self, mgr: BaseBlockManager, blkno: int) -> bool:
        """
        Checks if two blocks from two different block managers reference the
        same underlying values.
        """
        ref = weakref.ref(self.blocks[blkno])
        return ref in mgr.blocks[blkno].refs.referenced_blocks
