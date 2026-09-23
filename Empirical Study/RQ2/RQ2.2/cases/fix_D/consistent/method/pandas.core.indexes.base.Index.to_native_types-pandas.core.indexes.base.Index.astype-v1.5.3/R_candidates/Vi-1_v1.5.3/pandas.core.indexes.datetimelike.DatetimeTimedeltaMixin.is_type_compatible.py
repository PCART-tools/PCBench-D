    def is_type_compatible(self, kind: str) -> bool:
        warnings.warn(
            f"{type(self).__name__}.is_type_compatible is deprecated and will be "
            "removed in a future version.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return kind in self._data._infer_matches
