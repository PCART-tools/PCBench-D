    def delete(self, item):
        """
        Delete single item from SingleBlockManager.

        Ensures that self.blocks doesn't become empty.
        """
        loc = self.items.get_loc(item)
        self._block.delete(loc)
        self.axes[0] = self.axes[0].delete(loc)
