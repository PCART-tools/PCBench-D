    def __rpow__(self, other: Any) -> Series:
        return self.to_frame().select_seq(other ** F.col(self.name)).to_series()
