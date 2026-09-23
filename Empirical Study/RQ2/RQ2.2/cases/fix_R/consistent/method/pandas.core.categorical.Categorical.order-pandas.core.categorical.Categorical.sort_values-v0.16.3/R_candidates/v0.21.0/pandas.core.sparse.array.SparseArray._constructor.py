    @property
    def _constructor(self):
        return lambda x: SparseArray(x, fill_value=self.fill_value,
                                     kind=self.kind)
