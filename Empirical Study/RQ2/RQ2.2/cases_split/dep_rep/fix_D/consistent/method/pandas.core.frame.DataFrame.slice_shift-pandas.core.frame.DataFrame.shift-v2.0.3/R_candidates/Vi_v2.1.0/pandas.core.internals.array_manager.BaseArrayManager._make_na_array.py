    def _make_na_array(self, fill_value=None, use_na_proxy: bool = False):
        if use_na_proxy:
            assert fill_value is None
            return NullArrayProxy(self.shape_proper[0])

        if fill_value is None:
            fill_value = np.nan

        dtype, fill_value = infer_dtype_from_scalar(fill_value)
        array_values = make_na_array(dtype, self.shape_proper[:1], fill_value)
        return array_values
