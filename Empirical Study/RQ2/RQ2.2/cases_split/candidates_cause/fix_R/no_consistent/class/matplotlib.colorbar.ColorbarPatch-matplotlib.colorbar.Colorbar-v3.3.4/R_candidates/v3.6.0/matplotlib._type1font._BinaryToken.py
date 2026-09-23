class _BinaryToken(_Token):
    kind = 'binary'

    def value(self):
        return self.raw[1:]
