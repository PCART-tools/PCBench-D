    def __rsub__(self, other):
        return Index(other - np.array(self))
