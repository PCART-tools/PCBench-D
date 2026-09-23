    def diff(self: T, n: int, axis: AxisInt) -> T:
        # only reached with self.ndim == 2 and axis == 1
        axis = self._normalize_axis(axis)
        return self.apply("diff", n=n, axis=axis)
