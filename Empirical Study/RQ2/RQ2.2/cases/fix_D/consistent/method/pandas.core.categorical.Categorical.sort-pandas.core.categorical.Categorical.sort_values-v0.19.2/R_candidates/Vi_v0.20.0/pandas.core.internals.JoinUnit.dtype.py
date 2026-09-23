    @cache_readonly
    def dtype(self):
        if self.block is None:
            raise AssertionError("Block is None, no dtype")

        if not self.needs_filling:
            return self.block.dtype
        else:
            return _get_dtype(maybe_promote(self.block.dtype,
                                            self.block.fill_value)[0])

        return self._dtype
