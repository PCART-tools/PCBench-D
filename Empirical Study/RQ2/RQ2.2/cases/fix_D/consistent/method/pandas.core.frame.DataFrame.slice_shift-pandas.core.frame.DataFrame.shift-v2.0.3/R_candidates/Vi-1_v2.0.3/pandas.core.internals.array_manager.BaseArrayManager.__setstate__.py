    def __setstate__(self, state) -> None:
        self.arrays = state[0]
        self._axes = state[1]
