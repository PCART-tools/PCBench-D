    def peek(self, bits):
        while self.bits < bits:
            c = self.next()
            if c < 0:
                self.bits = 0
                continue
            self.bitbuffer = (self.bitbuffer << 8) + c
            self.bits += 8
        return self.bitbuffer >> (self.bits - bits) & (1 << bits) - 1
