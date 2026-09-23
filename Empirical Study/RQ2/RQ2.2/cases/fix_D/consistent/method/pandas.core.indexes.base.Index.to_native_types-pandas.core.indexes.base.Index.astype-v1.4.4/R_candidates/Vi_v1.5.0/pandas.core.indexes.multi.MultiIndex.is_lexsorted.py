    def is_lexsorted(self) -> bool:
        warnings.warn(
            "MultiIndex.is_lexsorted is deprecated as a public function, "
            "users should use MultiIndex.is_monotonic_increasing instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self._is_lexsorted()
