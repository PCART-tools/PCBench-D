    def get_numeric_data(self: T, copy: bool = False) -> T:
        """
        Parameters
        ----------
        copy : bool, default False
            Whether to copy the blocks
        """
        numeric_blocks = [blk for blk in self.blocks if blk.is_numeric]
        if len(numeric_blocks) == len(self.blocks):
            # Avoid somewhat expensive _combine
            if copy:
                return self.copy(deep=True)
            return self
        return self._combine(numeric_blocks, copy)
