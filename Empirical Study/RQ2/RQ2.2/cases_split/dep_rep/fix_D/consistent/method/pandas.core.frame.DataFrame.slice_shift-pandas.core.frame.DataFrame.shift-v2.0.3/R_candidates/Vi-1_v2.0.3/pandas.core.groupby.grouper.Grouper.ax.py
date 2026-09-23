    @final
    @property
    def ax(self) -> Index:
        warnings.warn(
            f"{type(self).__name__}.ax is deprecated and will be removed in a "
            "future version. Use Resampler.ax instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        index = self._gpr_index
        if index is None:
            raise ValueError("_set_grouper must be called before ax is accessed")
        return index
