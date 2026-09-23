    def data(self):
        s = self.fp.read(1)
        if s and s[0]:
            return self.fp.read(s[0])
        return None
