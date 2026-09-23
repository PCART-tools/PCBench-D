    def unique(self):
        from pandas import unique

        return type(self)(unique(self._ndarray))
