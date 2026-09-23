    @property
    def any_extension_types(self):
        """Whether any of the blocks in this manager are extension blocks"""
        return any(block.is_extension for block in self.blocks)
