    @property
    def is_single_block(self) -> bool:
        # Assumes we are 2D; overridden by SingleBlockManager
        return len(self.blocks) == 1
