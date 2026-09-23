    @property
    def lexsort_depth(self):
        warnings.warn(
            "MultiIndex.is_lexsorted is deprecated as a public function, "
            "users should use MultiIndex.is_monotonic_increasing instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self._lexsort_depth
