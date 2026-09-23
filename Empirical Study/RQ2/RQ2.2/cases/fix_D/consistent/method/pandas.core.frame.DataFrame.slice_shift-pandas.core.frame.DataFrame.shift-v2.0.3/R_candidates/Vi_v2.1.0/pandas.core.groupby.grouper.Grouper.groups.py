    @final
    @property
    def groups(self):
        warnings.warn(
            f"{type(self).__name__}.groups is deprecated and will be removed "
            "in a future version. Use GroupBy.groups instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        # error: "None" has no attribute "groups"
        return self._grouper_deprecated.groups  # type: ignore[attr-defined]
