    def view(self, dtype=None):
        return self._constructor(self.values.view(dtype),
                                 index=self.index).__finalize__(self)
