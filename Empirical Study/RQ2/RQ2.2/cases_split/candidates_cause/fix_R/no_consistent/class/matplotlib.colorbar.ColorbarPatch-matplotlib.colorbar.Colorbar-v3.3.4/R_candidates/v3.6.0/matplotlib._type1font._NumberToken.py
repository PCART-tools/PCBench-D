class _NumberToken(_Token):
    kind = 'number'

    def is_number(self):
        return True

    def value(self):
        if '.' not in self.raw:
            return int(self.raw)
        else:
            return float(self.raw)
