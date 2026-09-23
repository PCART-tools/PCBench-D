    @final
    def _find_common_type_compat(self, target) -> DtypeObj:
        """
        Implementation of find_common_type that adjusts for Index-specific
        special cases.
        """
        if is_interval_dtype(self.dtype) and is_valid_na_for_dtype(target, self.dtype):
            # e.g. setting NA value into IntervalArray[int64]
            self = cast("IntervalIndex", self)
            return IntervalDtype(np.float64, closed=self.closed)

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
                return np.dtype("object")

        dtype = find_common_type([self.dtype, target_dtype])

        if dtype.kind in ["i", "u"]:
            # TODO: what about reversed with self being categorical?
            if (
                isinstance(target, Index)
                and is_categorical_dtype(target.dtype)
                and target.hasnans
            ):
                # FIXME: find_common_type incorrect with Categorical GH#38240
                # FIXME: some cases where float64 cast can be lossy?
                dtype = np.dtype(np.float64)
        if dtype.kind == "c":
            dtype = np.dtype(object)
        return dtype
