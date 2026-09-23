    def __setstate__(self, state: bytes) -> None:
        self._pyexpr = F.lit(0)._pyexpr  # Initialize with a dummy
        self._pyexpr.__setstate__(state)
