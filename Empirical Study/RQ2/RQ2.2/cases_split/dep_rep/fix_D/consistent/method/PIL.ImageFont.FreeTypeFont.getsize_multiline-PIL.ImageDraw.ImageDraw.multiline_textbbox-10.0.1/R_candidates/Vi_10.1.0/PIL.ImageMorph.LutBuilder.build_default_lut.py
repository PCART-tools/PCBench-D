    def build_default_lut(self):
        symbols = [0, 1]
        m = 1 << 4  # pos of current pixel
        self.lut = bytearray(symbols[(i & m) > 0] for i in range(LUT_SIZE))
