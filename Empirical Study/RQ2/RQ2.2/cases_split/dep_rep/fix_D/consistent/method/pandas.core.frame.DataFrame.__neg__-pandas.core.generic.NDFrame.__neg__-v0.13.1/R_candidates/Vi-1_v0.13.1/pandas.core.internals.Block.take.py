    def take(self, indexer, ref_items, new_axis, axis=1):
        if axis < 1:
            raise AssertionError('axis must be at least 1, got %d' % axis)
        new_values = com.take_nd(self.values, indexer, axis=axis,
                                 allow_fill=False)

        # need to preserve the ref_locs and just shift them
        # GH6121
        ref_locs = None
        if not new_axis.is_unique:
            ref_locs = self._ref_locs

        return [make_block(new_values, self.items, ref_items, ndim=self.ndim,
                           klass=self.__class__, placement=ref_locs, fastpath=True)]
