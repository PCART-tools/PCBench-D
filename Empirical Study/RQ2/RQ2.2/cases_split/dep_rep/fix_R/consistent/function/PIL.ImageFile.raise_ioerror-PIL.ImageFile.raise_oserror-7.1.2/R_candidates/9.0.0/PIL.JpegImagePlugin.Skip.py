def Skip(self, marker):
    n = i16(self.fp.read(2)) - 2
    ImageFile._safe_read(self.fp, n)
