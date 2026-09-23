    def load_lut(self, filename: str) -> None:
        """Load an operator from an mrl file"""
        with open(filename, "rb") as f:
            self.lut = bytearray(f.read())

        if len(self.lut) != LUT_SIZE:
            self.lut = None
            msg = "Wrong size operator file!"
            raise Exception(msg)
