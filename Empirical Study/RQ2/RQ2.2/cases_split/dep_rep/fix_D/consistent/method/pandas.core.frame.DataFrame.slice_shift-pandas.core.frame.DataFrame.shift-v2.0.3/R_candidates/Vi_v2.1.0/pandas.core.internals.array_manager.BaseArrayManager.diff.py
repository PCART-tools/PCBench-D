    def diff(self, n: int) -> Self:
        assert self.ndim == 2  # caller ensures
        return self.apply(algos.diff, n=n)
