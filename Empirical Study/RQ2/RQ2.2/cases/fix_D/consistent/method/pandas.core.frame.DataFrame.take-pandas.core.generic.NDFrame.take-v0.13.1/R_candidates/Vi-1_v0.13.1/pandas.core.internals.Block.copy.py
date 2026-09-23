    def copy(self, deep=True, ref_items=None):
        values = self.values
        if deep:
            values = values.copy()
        if ref_items is None:
            ref_items = self.ref_items
        return make_block(values, self.items, ref_items, ndim=self.ndim,
                          klass=self.__class__, fastpath=True,
                          placement=self._ref_locs)
