    def concat_same_type(self, to_concat, placement=None):
        """
        Concatenate list of single blocks of the same type.
        """
        values = self._holder._concat_same_type([blk.values for blk in to_concat])
        placement = placement or slice(0, len(values), 1)
        return self.make_block_same_class(values, ndim=self.ndim, placement=placement)
