    def iget(self, i, fastpath=True):
        """
        Return the data as a SingleBlockManager if fastpath=True and possible

        Otherwise return as a ndarray
        """
        block = self.blocks[self._blknos[i]]
        values = block.iget(self._blklocs[i])
        if not fastpath or not block._box_to_block_values or values.ndim != 1:
            return values

        # fastpath shortcut for select a single-dim from a 2-dim BM
        return SingleBlockManager(
            [block.make_block_same_class(values,
                                         placement=slice(0, len(values)),
                                         ndim=1)],
            self.axes[1])
