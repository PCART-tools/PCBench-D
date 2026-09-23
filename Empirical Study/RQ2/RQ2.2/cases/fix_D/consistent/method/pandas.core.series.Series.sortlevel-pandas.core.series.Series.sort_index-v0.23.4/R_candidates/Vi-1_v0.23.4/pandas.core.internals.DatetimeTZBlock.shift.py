    def shift(self, periods, axis=0, mgr=None):
        """ shift the block by periods """

        # think about moving this to the DatetimeIndex. This is a non-freq
        # (number of periods) shift ###

        N = len(self)
        indexer = np.zeros(N, dtype=int)
        if periods > 0:
            indexer[periods:] = np.arange(N - periods)
        else:
            indexer[:periods] = np.arange(-periods, N)

        new_values = self.values.asi8.take(indexer)

        if periods > 0:
            new_values[:periods] = tslib.iNaT
        else:
            new_values[periods:] = tslib.iNaT

        new_values = self.values._shallow_copy(new_values)
        return [self.make_block_same_class(new_values,
                                           placement=self.mgr_locs)]
