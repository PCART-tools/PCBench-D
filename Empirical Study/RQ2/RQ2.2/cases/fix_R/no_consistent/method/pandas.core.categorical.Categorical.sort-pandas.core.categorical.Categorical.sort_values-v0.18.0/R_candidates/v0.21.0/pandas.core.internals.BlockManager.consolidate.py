    def consolidate(self):
        """
        Join together blocks having same dtype

        Returns
        -------
        y : BlockManager
        """
        if self.is_consolidated():
            return self

        bm = self.__class__(self.blocks, self.axes)
        bm._is_consolidated = False
        bm._consolidate_inplace()
        return bm
