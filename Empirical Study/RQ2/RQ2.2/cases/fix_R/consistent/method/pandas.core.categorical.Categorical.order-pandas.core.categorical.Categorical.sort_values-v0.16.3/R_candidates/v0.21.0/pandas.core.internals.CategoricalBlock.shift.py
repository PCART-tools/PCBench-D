    def shift(self, periods, axis=0, mgr=None):
        return self.make_block_same_class(values=self.values.shift(periods),
                                          placement=self.mgr_locs)
