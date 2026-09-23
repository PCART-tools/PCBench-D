    def diff(self, n, axis=1, mgr=None):
        """ return block for the diff of the values """
        new_values = algos.diff(self.values, n, axis=axis)
        return [self.make_block(values=new_values, fastpath=True)]
