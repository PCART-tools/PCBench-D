    def __array__(self, dtype: npt.DTypeLike | None = None) -> np.ndarray:
        values = self._values
        arr = np.asarray(values, dtype=dtype)
        if (
            astype_is_view(values.dtype, arr.dtype)
            and using_copy_on_write()
            and self._mgr.is_single_block
        ):
            # Check if both conversions can be done without a copy
            if astype_is_view(self.dtypes.iloc[0], values.dtype) and astype_is_view(
                values.dtype, arr.dtype
            ):
                arr = arr.view()
                arr.flags.writeable = False
        return arr
