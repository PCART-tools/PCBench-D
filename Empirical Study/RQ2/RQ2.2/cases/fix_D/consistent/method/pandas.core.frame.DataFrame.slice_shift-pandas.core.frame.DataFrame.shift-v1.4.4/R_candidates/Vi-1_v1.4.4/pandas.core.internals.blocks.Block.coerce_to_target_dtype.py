    @final
    def coerce_to_target_dtype(self, other) -> Block:
        """
        coerce the current block to a dtype compat for other
        we will return a block, possibly object, and not raise

        we can also safely try to coerce to the same dtype
        and will receive the same block
        """
        # if we cannot then coerce to object
        dtype, _ = infer_dtype_from(other, pandas_dtype=True)

        new_dtype = find_common_type([self.dtype, dtype])

        return self.astype(new_dtype, copy=False)
