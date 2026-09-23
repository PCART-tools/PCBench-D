    def concat_same_type(self, to_concat, placement=None):
        """
        Concatenate list of single blocks of the same type.
        """
        values = self._concatenator([blk.values for blk in to_concat],
                                    axis=self.ndim - 1)
        # not using self.make_block_same_class as values can be non-tz dtype
        return make_block(
            values, placement=placement or slice(0, len(values), 1))
