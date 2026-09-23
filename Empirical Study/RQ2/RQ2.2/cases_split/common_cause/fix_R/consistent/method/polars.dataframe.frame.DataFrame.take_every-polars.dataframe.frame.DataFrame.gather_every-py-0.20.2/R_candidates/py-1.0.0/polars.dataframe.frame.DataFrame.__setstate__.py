    def __setstate__(self, state: list[Series]) -> None:
        self._df = DataFrame(state)._df
