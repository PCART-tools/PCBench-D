    def copy(self, deep=True):
        values = self.values
        if deep:
            values = values.copy()
        return make_block(values, ndim=self.ndim,
                          klass=self.__class__, fastpath=True,
                          placement=self.mgr_locs)
