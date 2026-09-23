    def diff(self, n, axis=1):
        """ return block for the diff of the values """
        new_values = com.diff(self.values, n, axis=axis)
        return [make_block(values=new_values,
                           ndim=self.ndim, fastpath=True,
                           placement=self.mgr_locs)]
