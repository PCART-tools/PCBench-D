    def take(self, indexer, ref_items, axis=1):
        if axis < 1:
            raise AssertionError('axis must be at least 1, got %d' % axis)
        new_values = com.take_nd(self.values, indexer, axis=axis,
                                 allow_fill=False)
        return [make_block(new_values, self.items, ref_items, ndim=self.ndim,
                           klass=self.__class__, fastpath=True)]
