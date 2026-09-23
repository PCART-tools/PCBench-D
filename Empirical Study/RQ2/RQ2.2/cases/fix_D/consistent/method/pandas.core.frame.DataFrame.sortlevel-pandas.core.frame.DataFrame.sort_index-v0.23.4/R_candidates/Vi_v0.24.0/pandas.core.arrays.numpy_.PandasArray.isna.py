    def isna(self):
        from pandas import isna

        return isna(self._ndarray)
