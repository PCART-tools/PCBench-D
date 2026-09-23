    def copy(self, deep=True):
        """ copy constructor """
        values = self.values
        if deep:
            values = values.copy(deep=True)
        return self.make_block_same_class(values)
