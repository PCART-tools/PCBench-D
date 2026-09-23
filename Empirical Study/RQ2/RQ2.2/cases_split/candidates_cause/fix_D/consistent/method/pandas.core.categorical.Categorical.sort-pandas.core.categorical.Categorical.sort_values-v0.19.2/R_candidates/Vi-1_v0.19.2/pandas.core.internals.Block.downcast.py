    def downcast(self, dtypes=None, mgr=None):
        """ try to downcast each item to the dict of dtypes if present """

        # turn it off completely
        if dtypes is False:
            return self

        values = self.values

        # single block handling
        if self._is_single_block:

            # try to cast all non-floats here
            if dtypes is None:
                dtypes = 'infer'

            nv = _possibly_downcast_to_dtype(values, dtypes)
            return self.make_block(nv, fastpath=True)

        # ndim > 1
        if dtypes is None:
            return self

        if not (dtypes == 'infer' or isinstance(dtypes, dict)):
            raise ValueError("downcast must have a dictionary or 'infer' as "
                             "its argument")

        # item-by-item
        # this is expensive as it splits the blocks items-by-item
        blocks = []
        for i, rl in enumerate(self.mgr_locs):

            if dtypes == 'infer':
                dtype = 'infer'
            else:
                raise AssertionError("dtypes as dict is not supported yet")
                # TODO: This either should be completed or removed
                dtype = dtypes.get(item, self._downcast_dtype)  # noqa

            if dtype is None:
                nv = _block_shape(values[i], ndim=self.ndim)
            else:
                nv = _possibly_downcast_to_dtype(values[i], dtype)
                nv = _block_shape(nv, ndim=self.ndim)

            blocks.append(self.make_block(nv, fastpath=True, placement=[rl]))

        return blocks
