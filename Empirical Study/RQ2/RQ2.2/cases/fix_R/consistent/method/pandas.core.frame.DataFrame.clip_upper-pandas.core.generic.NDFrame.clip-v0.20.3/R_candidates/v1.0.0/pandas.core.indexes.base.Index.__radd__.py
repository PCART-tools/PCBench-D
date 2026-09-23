    def __radd__(self, other):
        from pandas import Series

        return Index(other + Series(self))
