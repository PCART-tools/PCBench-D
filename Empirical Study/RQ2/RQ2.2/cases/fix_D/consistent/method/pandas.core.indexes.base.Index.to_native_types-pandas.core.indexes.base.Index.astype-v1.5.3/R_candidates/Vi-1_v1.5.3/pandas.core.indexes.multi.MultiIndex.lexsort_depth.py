    @property
    def lexsort_depth(self) -> int:
        warnings.warn(
            "MultiIndex.lexsort_depth is deprecated as a public function, "
            "users should use MultiIndex.is_monotonic_increasing instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._lexsort_depth
