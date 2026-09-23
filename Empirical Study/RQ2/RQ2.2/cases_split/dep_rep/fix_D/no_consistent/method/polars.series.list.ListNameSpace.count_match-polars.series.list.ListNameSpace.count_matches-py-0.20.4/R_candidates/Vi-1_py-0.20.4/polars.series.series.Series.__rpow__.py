    def __rpow__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            msg = "first cast to integer before raising datelike dtypes to a power"
            raise TypeError(msg)
        return self.to_frame().select_seq(other ** F.col(self.name)).to_series()
