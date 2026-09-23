    @final
    def _find_common_type_compat(self, target) -> DtypeObj:
        """
        Implementation of find_common_type that adjusts for Index-specific
        special cases.
        """
        if is_valid_na_for_dtype(target, self.dtype):
            # e.g. setting NA value into IntervalArray[int64]
            dtype = ensure_dtype_can_hold_na(self.dtype)
            if is_dtype_equal(self.dtype, dtype):
                raise NotImplementedError(
                    "This should not be reached. Please report a bug at "
                    "github.com/pandas-dev/pandas"
                )
            return dtype

        target_dtype, _ = infer_dtype_from(target, pandas_dtype=True)

        # special case: if one dtype is uint64 and the other a signed int, return object
        # See https://github.com/pandas-dev/pandas/issues/26778 for discussion
        # Now it's:
        # * float | [u]int -> float
        # * uint64 | signed int  -> object
        # We may change union(float | [u]int) to go to object.
        if self.dtype == "uint64" or target_dtype == "uint64":
            if is_signed_integer_dtype(self.dtype) or is_signed_integer_dtype(
                target_dtype
            ):
                return _dtype_obj

        dtype = find_common_type([self.dtype, target_dtype])
        dtype = common_dtype_categorical_compat([self, target], dtype)
        return dtype
