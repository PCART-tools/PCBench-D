    @property
    @doc(Series.is_monotonic_increasing.__doc__)
    def is_monotonic_increasing(self) -> Series:
        return self.apply(lambda ser: ser.is_monotonic_increasing)
