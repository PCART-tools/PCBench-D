    def save_lut(self, filename: str) -> None:
        """Save an operator to an mrl file"""
        if self.lut is None:
            msg = "No operator loaded"
            raise Exception(msg)
        with open(filename, "wb") as f:
            f.write(self.lut)
