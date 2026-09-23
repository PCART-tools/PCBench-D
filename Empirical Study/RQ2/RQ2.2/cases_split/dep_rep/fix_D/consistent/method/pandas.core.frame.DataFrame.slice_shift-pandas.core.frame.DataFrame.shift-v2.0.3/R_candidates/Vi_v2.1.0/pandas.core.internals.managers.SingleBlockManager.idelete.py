    def idelete(self, indexer) -> SingleBlockManager:
        """
        Delete single location from SingleBlockManager.

        Ensures that self.blocks doesn't become empty.
        """
        nb = self._block.delete(indexer)[0]
        self.blocks = (nb,)
        self.axes[0] = self.axes[0].delete(indexer)
        self._cache.clear()
        return self
