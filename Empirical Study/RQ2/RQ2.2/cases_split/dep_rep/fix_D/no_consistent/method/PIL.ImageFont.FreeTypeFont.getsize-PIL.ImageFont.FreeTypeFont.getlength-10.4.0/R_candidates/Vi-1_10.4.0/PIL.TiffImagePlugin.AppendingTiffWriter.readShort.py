    def readShort(self) -> int:
        (value,) = struct.unpack(self.shortFmt, self.f.read(2))
        return value
