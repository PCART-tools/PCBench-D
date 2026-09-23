    def _delete_from_block(self, i, item):
        super(SingleBlockManager, self)._delete_from_block(i, item)

        # reset our state
        self._block = (
            self.blocks[0] if len(self.blocks) else
            make_block(np.array([], dtype=self._block.dtype), [], [])
        )
        self._values = self._block.values
