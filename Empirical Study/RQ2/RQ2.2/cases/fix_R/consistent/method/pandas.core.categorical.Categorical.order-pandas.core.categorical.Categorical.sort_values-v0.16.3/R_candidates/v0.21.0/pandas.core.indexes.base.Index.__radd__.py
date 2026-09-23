    def __radd__(self, other):
        return Index(other + np.array(self))
