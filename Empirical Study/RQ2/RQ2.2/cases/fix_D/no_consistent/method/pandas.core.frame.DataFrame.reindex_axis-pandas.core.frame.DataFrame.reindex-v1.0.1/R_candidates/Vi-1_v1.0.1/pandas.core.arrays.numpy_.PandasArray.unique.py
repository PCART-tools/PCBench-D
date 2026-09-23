    def unique(self):
        return type(self)(unique(self._ndarray))
