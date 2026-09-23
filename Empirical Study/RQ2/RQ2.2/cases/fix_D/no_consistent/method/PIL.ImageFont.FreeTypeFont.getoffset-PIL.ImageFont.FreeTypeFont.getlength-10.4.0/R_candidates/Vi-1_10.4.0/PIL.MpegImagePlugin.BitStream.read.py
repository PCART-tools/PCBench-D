    def read(self, bits: int) -> int:
        v = self.peek(bits)
        self.bits = self.bits - bits
        return v
