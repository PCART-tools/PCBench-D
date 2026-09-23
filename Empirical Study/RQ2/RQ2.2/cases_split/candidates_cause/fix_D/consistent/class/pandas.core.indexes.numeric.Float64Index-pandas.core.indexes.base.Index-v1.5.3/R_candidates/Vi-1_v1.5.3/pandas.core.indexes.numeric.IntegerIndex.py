class IntegerIndex(NumericIndex):
    """
    This is an abstract class for Int64Index, UInt64Index.
    """

    _is_backward_compat_public_numeric_index: bool = False

    @property
    def asi8(self) -> npt.NDArray[np.int64]:
        # do not cache or you'll create a memory leak
        warnings.warn(
            "Index.asi8 is deprecated and will be removed in a future version.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._values.view(self._default_dtype)
