    def setitem(self, indexer, value):
        # https://github.com/pandas-dev/pandas/issues/24020
        # Need a dedicated setitem until #24020 (type promotion in setitem
        # for extension arrays) is designed and implemented.
        try:
            return super(DatetimeTZBlock, self).setitem(indexer, value)
        except (ValueError, TypeError):
            newb = make_block(self.values.astype(object),
                              placement=self.mgr_locs,
                              klass=ObjectBlock,)
            return newb.setitem(indexer, value)
