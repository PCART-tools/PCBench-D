    def write(self, data: bytes) -> None:
        self.chunk(self.fp, b"IDAT", data)
