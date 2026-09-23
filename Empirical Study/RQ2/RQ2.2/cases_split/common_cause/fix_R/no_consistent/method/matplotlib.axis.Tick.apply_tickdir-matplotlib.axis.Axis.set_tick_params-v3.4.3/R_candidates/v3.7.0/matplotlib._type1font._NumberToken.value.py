    def value(self):
        if '.' not in self.raw:
            return int(self.raw)
        else:
            return float(self.raw)
