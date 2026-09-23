    @cache_readonly
    def dtype(self) -> DtypeObj:
        blk = self.block
        if blk.values.dtype.kind == "V":
            raise AssertionError("Block is None, no dtype")

        if not self.needs_filling:
            return blk.dtype
        return ensure_dtype_can_hold_na(blk.dtype)
