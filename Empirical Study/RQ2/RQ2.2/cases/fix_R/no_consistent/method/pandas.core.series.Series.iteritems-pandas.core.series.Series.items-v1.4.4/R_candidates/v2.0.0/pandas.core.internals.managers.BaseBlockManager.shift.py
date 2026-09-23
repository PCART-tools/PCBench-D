    def shift(self: T, periods: int, axis: AxisInt, fill_value) -> T:
        axis = self._normalize_axis(axis)
        if fill_value is lib.no_default:
            fill_value = None

        return self.apply("shift", periods=periods, axis=axis, fill_value=fill_value)
