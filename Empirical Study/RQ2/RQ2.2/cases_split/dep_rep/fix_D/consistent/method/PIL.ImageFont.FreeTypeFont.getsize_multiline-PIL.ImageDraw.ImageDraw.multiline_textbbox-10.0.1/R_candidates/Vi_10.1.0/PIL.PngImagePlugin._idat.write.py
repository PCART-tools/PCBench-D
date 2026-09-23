    def write(self, data):
        self.chunk(self.fp, b"IDAT", data)
