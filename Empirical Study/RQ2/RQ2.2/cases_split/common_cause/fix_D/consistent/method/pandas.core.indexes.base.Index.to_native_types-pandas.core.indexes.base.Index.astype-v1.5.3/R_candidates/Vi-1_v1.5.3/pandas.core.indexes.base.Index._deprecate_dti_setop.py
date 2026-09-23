    @final
    def _deprecate_dti_setop(self, other: Index, setop: str_t):
        """
        Deprecate setop behavior between timezone-aware DatetimeIndexes with
        mismatched timezones.
        """
        # Caller is responsibelf or checking
        #  `not is_dtype_equal(self.dtype, other.dtype)`
        if (
            isinstance(self, ABCDatetimeIndex)
            and isinstance(other, ABCDatetimeIndex)
            and self.tz is not None
            and other.tz is not None
        ):
            # GH#39328, GH#45357
            warnings.warn(
                f"In a future version, the {setop} of DatetimeIndex objects "
                "with mismatched timezones will cast both to UTC instead of "
                "object dtype. To retain the old behavior, "
                f"use `index.astype(object).{setop}(other)`",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
