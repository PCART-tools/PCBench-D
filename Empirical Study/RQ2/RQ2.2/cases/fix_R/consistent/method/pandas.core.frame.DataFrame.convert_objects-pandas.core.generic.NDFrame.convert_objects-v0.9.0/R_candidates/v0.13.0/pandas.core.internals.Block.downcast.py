    def downcast(self, dtypes=None):
        """ try to downcast each item to the dict of dtypes if present """

        # turn it off completely
        if dtypes is False:
            return [self]

        values = self.values

        # single block handling
        if self._is_single_block:

            # try to cast all non-floats here
            if dtypes is None:
                dtypes = 'infer'

            nv = _possibly_downcast_to_dtype(values, dtypes)
            return [make_block(nv, self.items, self.ref_items, ndim=self.ndim,
                               fastpath=True)]

        # ndim > 1
        if dtypes is None:
            return [self]

        if not (dtypes == 'infer' or isinstance(dtypes, dict)):
            raise ValueError("downcast must have a dictionary or 'infer' as "
                             "its argument")

        # item-by-item
        # this is expensive as it splits the blocks items-by-item
        blocks = []
        for i, item in enumerate(self.items):

            if dtypes == 'infer':
                dtype = 'infer'
            else:
                dtype = dtypes.get(item, self._downcast_dtype)

            if dtype is None:
                nv = _block_shape(values[i], ndim=self.ndim)
            else:
                nv = _possibly_downcast_to_dtype(values[i], dtype)
                nv = _block_shape(nv, ndim=self.ndim)

            blocks.append(make_block(nv, Index([item]), self.ref_items,
                                     ndim=self.ndim, fastpath=True))

        return blocks
