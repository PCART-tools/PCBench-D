    def iget(self, i):
        """
        Return the data as a SingleBlockManager if possible

        Otherwise return as a ndarray
        """
        block = self.blocks[self._blknos[i]]
        values = block.iget(self._blklocs[i])

        # shortcut for select a single-dim from a 2-dim BM
        return SingleBlockManager(
            [
                block.make_block_same_class(
                    values, placement=slice(0, len(values)), ndim=1
                )
            ],
            self.axes[1],
        )
