    @cache_readonly
    def _data(self) -> np.ndarray:  # type: ignore[override]
        """
        An int array that for performance reasons is created only when needed.

        The constructed array is saved in ``_cache``.
        """
        return np.arange(self.start, self.stop, self.step, dtype=np.int64)
