    def __sub__(self, other):
        return Index(np.array(self) - other)
