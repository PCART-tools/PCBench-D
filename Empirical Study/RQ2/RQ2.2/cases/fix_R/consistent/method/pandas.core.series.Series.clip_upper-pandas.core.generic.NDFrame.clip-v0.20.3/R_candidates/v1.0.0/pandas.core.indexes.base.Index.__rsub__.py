    def __rsub__(self, other):
        # wrap Series to ensure we pin name correctly
        from pandas import Series

        return Index(other - Series(self))
