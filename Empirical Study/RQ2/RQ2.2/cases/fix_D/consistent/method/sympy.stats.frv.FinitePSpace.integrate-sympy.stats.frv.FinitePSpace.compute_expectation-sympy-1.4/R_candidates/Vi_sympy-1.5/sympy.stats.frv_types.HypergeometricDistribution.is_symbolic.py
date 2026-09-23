    @property
    def is_symbolic(self):
        return any(not x.is_number for x in (self.N, self.m, self.n))
