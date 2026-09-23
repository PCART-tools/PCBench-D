    def copy(self, deep=True):
        return self.make_block_same_class(values=self.values,
                                          sparse_index=self.sp_index,
                                          kind=self.kind, copy=deep,
                                          placement=self.mgr_locs)
