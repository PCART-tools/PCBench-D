    def read(self, bits):
        v = self.peek(bits)
        self.bits = self.bits - bits
        return v
