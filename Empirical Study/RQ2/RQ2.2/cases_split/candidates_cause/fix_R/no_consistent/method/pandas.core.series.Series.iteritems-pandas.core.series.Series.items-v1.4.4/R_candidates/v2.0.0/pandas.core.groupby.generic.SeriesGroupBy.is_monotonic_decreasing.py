    @property
    @doc(Series.is_monotonic_decreasing.__doc__)
    def is_monotonic_decreasing(self) -> Series:
        return self.apply(lambda ser: ser.is_monotonic_decreasing)
