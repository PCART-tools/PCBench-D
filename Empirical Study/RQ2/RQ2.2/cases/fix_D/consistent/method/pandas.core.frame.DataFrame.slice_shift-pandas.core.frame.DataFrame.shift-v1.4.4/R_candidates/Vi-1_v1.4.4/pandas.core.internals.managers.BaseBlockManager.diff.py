    def diff(self: T, n: int, axis: int) -> T:
        axis = self._normalize_axis(axis)
        return self.apply("diff", n=n, axis=axis)
