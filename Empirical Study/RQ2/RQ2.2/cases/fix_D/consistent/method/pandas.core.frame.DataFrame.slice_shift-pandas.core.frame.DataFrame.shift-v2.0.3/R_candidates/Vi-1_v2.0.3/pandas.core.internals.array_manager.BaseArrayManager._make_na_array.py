    def _make_na_array(self, fill_value=None, use_na_proxy: bool = False):
        if use_na_proxy:
            assert fill_value is None
            return NullArrayProxy(self.shape_proper[0])

        if fill_value is None:
            fill_value = np.nan

        dtype, fill_value = infer_dtype_from_scalar(fill_value)
        # error: Argument "dtype" to "empty" has incompatible type "Union[dtype[Any],
        # ExtensionDtype]"; expected "Union[dtype[Any], None, type, _SupportsDType, str,
        # Union[Tuple[Any, int], Tuple[Any, Union[int, Sequence[int]]], List[Any],
        # _DTypeDict, Tuple[Any, Any]]]"
        values = np.empty(self.shape_proper[0], dtype=dtype)  # type: ignore[arg-type]
        values.fill(fill_value)
        return values
