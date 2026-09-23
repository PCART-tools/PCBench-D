    def setitem(self, indexer, value):
        # https://github.com/pandas-dev/pandas/issues/24020
        # Need a dedicated setitem until #24020 (type promotion in setitem
        # for extension arrays) is designed and implemented.
        if self._can_hold_element(value) or (
            isinstance(indexer, np.ndarray) and indexer.size == 0
        ):
            return super().setitem(indexer, value)

        obj_vals = self.values.astype(object)
        newb = make_block(
            obj_vals, placement=self.mgr_locs, klass=ObjectBlock, ndim=self.ndim
        )
        return newb.setitem(indexer, value)
