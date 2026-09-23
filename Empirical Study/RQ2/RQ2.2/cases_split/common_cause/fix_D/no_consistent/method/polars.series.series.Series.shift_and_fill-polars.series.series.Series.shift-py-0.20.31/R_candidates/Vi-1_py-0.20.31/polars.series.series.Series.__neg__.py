    def __neg__(self) -> Series:
        return self.to_frame().select_seq(-F.col(self.name)).to_series()
