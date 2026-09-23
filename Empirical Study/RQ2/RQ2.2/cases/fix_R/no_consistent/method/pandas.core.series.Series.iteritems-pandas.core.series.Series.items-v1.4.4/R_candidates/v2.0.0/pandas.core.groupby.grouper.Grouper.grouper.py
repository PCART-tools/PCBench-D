    @final
    @property
    def grouper(self):
        warnings.warn(
            f"{type(self).__name__}.grouper is deprecated and will be removed "
            "in a future version. Use GroupBy.grouper instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._grouper_deprecated
