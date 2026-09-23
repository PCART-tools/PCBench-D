    @cache_readonly
    def is_sparse(self):
        return self.block is not None and self.block.is_sparse
