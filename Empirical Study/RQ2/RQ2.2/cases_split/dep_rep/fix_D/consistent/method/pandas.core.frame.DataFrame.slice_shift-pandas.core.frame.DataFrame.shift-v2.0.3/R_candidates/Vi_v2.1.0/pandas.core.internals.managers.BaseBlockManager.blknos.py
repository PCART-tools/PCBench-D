    @property
    def blknos(self) -> npt.NDArray[np.intp]:
        """
        Suppose we want to find the array corresponding to our i'th column.

        blknos[i] identifies the block from self.blocks that contains this column.

        blklocs[i] identifies the column of interest within
        self.blocks[self.blknos[i]]
        """
        if self._blknos is None:
            # Note: these can be altered by other BlockManager methods.
            self._rebuild_blknos_and_blklocs()

        return self._blknos
