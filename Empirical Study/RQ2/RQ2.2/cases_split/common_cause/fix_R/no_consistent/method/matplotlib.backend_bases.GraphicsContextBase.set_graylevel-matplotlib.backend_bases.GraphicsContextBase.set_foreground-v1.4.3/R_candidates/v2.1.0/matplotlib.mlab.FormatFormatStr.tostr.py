    def tostr(self, x):
        if x is None:
            return 'None'
        return self.fmt % self.toval(x)
