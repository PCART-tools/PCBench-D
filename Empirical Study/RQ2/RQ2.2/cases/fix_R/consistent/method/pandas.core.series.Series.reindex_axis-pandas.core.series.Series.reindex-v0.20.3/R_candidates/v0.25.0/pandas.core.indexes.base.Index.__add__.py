    def __add__(self, other):
        if isinstance(other, (ABCSeries, ABCDataFrame)):
            return NotImplemented
        from pandas import Series

        return Index(Series(self) + other)
