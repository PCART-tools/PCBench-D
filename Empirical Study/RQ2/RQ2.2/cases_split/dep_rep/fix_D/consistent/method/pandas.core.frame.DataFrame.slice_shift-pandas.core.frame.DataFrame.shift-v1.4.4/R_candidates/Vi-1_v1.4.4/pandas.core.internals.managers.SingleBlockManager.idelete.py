    def idelete(self, indexer) -> SingleBlockManager:
        """
        Delete single location from SingleBlockManager.

        Ensures that self.blocks doesn't become empty.
        """
        self._block.delete(indexer)
        self.axes[0] = self.axes[0].delete(indexer)
        return self
