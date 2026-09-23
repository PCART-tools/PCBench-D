    @final
    def coerce_to_target_dtype(self, other, warn_on_upcast: bool = False) -> Block:
        """
        coerce the current block to a dtype compat for other
        we will return a block, possibly object, and not raise

        we can also safely try to coerce to the same dtype
        and will receive the same block
        """
        new_dtype = find_result_type(self.values.dtype, other)

        # In a future version of pandas, the default will be that
        # setting `nan` into an integer series won't raise.
        if (
            is_scalar(other)
            and is_integer_dtype(self.values.dtype)
            and isna(other)
            and other is not NaT
        ):
            warn_on_upcast = False
        elif (
            isinstance(other, np.ndarray)
            and other.ndim == 1
            and is_integer_dtype(self.values.dtype)
            and is_float_dtype(other.dtype)
            and lib.has_only_ints_or_nan(other)
        ):
            warn_on_upcast = False

        if warn_on_upcast:
            warnings.warn(
                f"Setting an item of incompatible dtype is deprecated "
                "and will raise in a future error of pandas. "
                f"Value '{other}' has dtype incompatible with {self.values.dtype}, "
                "please explicitly cast to a compatible dtype first.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if self.values.dtype == new_dtype:
            raise AssertionError(
                f"Did not expect new dtype {new_dtype} to equal self.dtype "
                f"{self.values.dtype}. Please report a bug at "
                "https://github.com/pandas-dev/pandas/issues."
            )
        return self.astype(new_dtype, copy=False)
