    def write(self, data: bytes) -> None:
        self.chunk(self.fp, b"fdAT", o32(self.seq_num), data)
        self.seq_num += 1
