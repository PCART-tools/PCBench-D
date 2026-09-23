    def readShort(self):
        (value,) = struct.unpack(self.shortFmt, self.f.read(2))
        return value
