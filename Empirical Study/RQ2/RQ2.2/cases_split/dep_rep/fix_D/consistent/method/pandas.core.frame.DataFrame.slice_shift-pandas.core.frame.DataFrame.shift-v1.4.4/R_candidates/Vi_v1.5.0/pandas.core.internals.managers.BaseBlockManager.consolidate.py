    def consolidate(self: T) -> T:
        """
        Join together blocks having same dtype

        Returns
        -------
        y : BlockManager
        """
        if self.is_consolidated():
            return self

        bm = type(self)(self.blocks, self.axes, self.refs, verify_integrity=False)
        bm._is_consolidated = False
        bm._consolidate_inplace()
        return bm
