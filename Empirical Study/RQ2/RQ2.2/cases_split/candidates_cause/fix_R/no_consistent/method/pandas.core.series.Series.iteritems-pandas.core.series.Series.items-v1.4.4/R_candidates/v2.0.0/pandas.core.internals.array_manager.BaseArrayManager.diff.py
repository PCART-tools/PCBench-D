    def diff(self: T, n: int, axis: AxisInt) -> T:
        assert self.ndim == 2 and axis == 0  # caller ensures
        return self.apply(algos.diff, n=n, axis=axis)
