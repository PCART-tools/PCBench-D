    def _mpl_repr(self):
        # how to represent ourselves to matplotlib
        return self.astype(object)._values
