    @property
    def asi8(self) -> np.ndarray:
        # do not cache or you'll create a memory leak
        warnings.warn(
            "Index.asi8 is deprecated and will be removed in a future version",
            FutureWarning,
            stacklevel=2,
        )
        return self._values.view(self._default_dtype)
