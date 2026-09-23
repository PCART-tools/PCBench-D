    def copy(self, deep=True, mgr=None):
        """ copy constructor """
        values = self.values
        if deep:
            values = values.copy(deep=True)
        return self.make_block_same_class(values)
