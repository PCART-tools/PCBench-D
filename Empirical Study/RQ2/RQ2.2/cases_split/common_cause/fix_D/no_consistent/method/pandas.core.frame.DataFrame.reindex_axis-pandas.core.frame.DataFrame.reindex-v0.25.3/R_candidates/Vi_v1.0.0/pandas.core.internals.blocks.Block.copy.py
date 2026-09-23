    def copy(self, deep=True):
        """ copy constructor """
        values = self.values
        if deep:
            values = values.copy()
        return self.make_block_same_class(values, ndim=self.ndim)
