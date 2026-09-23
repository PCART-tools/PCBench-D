    def setEndian(self, endian: str) -> None:
        self.endian = endian
        self.longFmt = f"{self.endian}L"
        self.shortFmt = f"{self.endian}H"
        self.tagFormat = f"{self.endian}HHL"
