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
        block_shape = list(self.shape)
        block_shape[0] = len(placement)

        dtype, fill_value = infer_dtype_from_scalar(fill_value)
        # error: Argument "dtype" to "empty" has incompatible type "Union[dtype,
        # ExtensionDtype]"; expected "Union[dtype, None, type, _SupportsDtype, str,
        # Tuple[Any, int], Tuple[Any, Union[int, Sequence[int]]], List[Any], _DtypeDict,
        # Tuple[Any, Any]]"
        block_values = np.empty(block_shape, dtype=dtype)  # type: ignore[arg-type]
        block_values.fill(fill_value)
        return new_block_2d(block_values, placement=placement)
