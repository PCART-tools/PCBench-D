    def readLong(self) -> int:
        (value,) = struct.unpack(self.longFmt, self.f.read(4))
        return value
