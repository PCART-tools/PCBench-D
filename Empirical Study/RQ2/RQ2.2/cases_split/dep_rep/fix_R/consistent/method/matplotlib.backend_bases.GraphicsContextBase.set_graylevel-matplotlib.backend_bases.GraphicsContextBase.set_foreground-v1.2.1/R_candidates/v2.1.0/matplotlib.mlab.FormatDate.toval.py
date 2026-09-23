    def toval(self, x):
        if x is None:
            return 'None'
        return x.strftime(self.fmt)
