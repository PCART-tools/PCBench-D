    def __setstate__(self, state: bytes) -> None:
        self._ldf = LazyFrame()._ldf  # Initialize with a dummy
        self._ldf.__setstate__(state)
