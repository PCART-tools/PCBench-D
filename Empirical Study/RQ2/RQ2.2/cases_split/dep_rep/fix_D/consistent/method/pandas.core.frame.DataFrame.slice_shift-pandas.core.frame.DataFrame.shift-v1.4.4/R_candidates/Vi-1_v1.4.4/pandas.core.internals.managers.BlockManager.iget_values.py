    def iget_values(self, i: int) -> ArrayLike:
        """
        Return the data for column i as the values (ndarray or ExtensionArray).
        """
        block = self.blocks[self.blknos[i]]
        values = block.iget(self.blklocs[i])
        return values
