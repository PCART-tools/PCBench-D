    @property
    def asi8(self) -> npt.NDArray[np.int64]:
        # do not cache or you'll create a memory leak
        warnings.warn(
            "Index.asi8 is deprecated and will be removed in a future version.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self._values.view(self._default_dtype)
