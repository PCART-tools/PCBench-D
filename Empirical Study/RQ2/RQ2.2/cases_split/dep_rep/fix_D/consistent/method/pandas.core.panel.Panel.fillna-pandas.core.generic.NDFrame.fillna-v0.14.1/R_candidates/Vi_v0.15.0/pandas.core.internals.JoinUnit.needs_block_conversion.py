    @cache_readonly
    def needs_block_conversion(self):
        """ we might need to convert the joined values to a suitable block repr """
        block = self.block
        return block is not None and (block.is_sparse or block.is_categorical)
