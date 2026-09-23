    @cache_readonly
    def is_na(self) -> bool:
        blk = self.block
        if blk.dtype.kind == "V":
            return True

        if not blk._can_hold_na:
            return False

        values = blk.values
        if values.size == 0:
            return True
        if isinstance(values.dtype, SparseDtype):
            return False

        if values.ndim == 1:
            # TODO(EA2D): no need for special case with 2D EAs
            val = values[0]
            if not is_scalar(val) or not isna(val):
                # ideally isna_all would do this short-circuiting
                return False
            return isna_all(values)
        else:
            val = values[0][0]
            if not is_scalar(val) or not isna(val):
                # ideally isna_all would do this short-circuiting
                return False
            return all(isna_all(row) for row in values)
