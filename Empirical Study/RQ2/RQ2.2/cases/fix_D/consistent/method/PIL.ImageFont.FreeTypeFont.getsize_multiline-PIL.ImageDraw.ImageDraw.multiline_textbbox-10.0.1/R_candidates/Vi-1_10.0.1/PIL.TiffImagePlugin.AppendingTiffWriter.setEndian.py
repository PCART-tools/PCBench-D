    def setEndian(self, endian):
        self.endian = endian
        self.longFmt = self.endian + "L"
        self.shortFmt = self.endian + "H"
        self.tagFormat = self.endian + "HHL"
