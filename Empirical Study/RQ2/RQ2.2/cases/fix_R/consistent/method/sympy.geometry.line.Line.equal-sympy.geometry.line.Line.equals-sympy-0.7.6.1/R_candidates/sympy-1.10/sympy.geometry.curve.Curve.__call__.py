    def __call__(self, f):
        return self.subs(self.parameter, f)
