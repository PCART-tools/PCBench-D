    def __add__(self, other):
        return Index(np.array(self) + other)
