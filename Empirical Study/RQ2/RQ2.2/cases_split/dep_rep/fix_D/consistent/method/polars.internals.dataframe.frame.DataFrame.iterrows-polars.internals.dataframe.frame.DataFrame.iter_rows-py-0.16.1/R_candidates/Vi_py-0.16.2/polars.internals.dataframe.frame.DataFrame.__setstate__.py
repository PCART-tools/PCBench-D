    def __setstate__(self, state) -> None:  # type: ignore[no-untyped-def]
        self._df = DataFrame(state)._df
