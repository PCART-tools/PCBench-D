    def view(self, dtype=None):
        return self._constructor(self._values.view(dtype),
                                 index=self.index).__finalize__(self)
