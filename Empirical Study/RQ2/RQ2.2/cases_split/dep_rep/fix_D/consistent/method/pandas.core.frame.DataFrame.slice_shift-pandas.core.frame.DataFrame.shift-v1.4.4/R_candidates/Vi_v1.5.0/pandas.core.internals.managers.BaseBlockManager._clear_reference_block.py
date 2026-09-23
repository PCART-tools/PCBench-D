    def _clear_reference_block(self, blkno: int) -> None:
        """
        Clear any reference for column `i`.
        """
        if self.refs is not None:
            self.refs[blkno] = None
