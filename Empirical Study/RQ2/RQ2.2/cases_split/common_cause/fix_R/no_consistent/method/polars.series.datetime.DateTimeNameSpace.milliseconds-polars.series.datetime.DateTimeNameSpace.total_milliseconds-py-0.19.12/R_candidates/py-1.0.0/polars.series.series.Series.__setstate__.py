    def __setstate__(self, state: bytes) -> None:
        self._s = Series()._s  # Initialize with a dummy
        self._s.__setstate__(state)
