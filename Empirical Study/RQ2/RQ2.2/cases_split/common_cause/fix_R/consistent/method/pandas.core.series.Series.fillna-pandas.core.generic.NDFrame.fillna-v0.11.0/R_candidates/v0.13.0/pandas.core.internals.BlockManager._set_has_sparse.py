    def _set_has_sparse(self):
        self._has_sparse = any((blk.is_sparse for blk in self.blocks))
