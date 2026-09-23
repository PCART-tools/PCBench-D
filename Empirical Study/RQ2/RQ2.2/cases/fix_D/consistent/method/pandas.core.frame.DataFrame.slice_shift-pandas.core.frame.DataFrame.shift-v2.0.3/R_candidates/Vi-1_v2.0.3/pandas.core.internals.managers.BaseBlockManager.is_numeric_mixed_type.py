    @property
    def is_numeric_mixed_type(self) -> bool:
        return all(block.is_numeric for block in self.blocks)
