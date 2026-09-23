    def _make_na_block(
        self, placement: BlockPlacement, fill_value=None, use_na_proxy: bool = False
    ) -> Block:
        # Note: we only get here with self.ndim == 2

        if use_na_proxy:
            assert fill_value is None
            shape = (len(placement), self.shape[1])
            vals = np.empty(shape, dtype=np.void)
            nb = NumpyBlock(vals, placement, ndim=2)
            return nb

        if fill_value is None:
            fill_value = np.nan

        shape = (len(placement), self.shape[1])

        dtype, fill_value = infer_dtype_from_scalar(fill_value)
        block_values = make_na_array(dtype, shape, fill_value)
        return new_block_2d(block_values, placement=placement)
