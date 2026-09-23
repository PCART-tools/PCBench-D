    def __add__(self, other):
        if isinstance(other, (ABCSeries, ABCDataFrame)):
            return NotImplemented
        return Index(np.array(self) + other)
