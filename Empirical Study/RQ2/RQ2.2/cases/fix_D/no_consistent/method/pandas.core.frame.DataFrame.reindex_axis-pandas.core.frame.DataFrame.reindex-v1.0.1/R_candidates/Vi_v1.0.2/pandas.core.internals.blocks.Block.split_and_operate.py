    def split_and_operate(self, mask, f, inplace: bool):
        """
        split the block per-column, and apply the callable f
        per-column, return a new block for each. Handle
        masking which will not change a block unless needed.

        Parameters
        ----------
        mask : 2-d boolean mask
        f : callable accepting (1d-mask, 1d values, indexer)
        inplace : boolean

        Returns
        -------
        list of blocks
        """

        if mask is None:
            mask = np.broadcast_to(True, shape=self.shape)

        new_values = self.values

        def make_a_block(nv, ref_loc):
            if isinstance(nv, list):
                assert len(nv) == 1, nv
                assert isinstance(nv[0], Block)
                block = nv[0]
            else:
                # Put back the dimension that was taken from it and make
                # a block out of the result.
                nv = _block_shape(nv, ndim=self.ndim)
                block = self.make_block(values=nv, placement=ref_loc)
            return block

        # ndim == 1
        if self.ndim == 1:
            if mask.any():
                nv = f(mask, new_values, None)
            else:
                nv = new_values if inplace else new_values.copy()
            block = make_a_block(nv, self.mgr_locs)
            return [block]

        # ndim > 1
        new_blocks = []
        for i, ref_loc in enumerate(self.mgr_locs):
            m = mask[i]
            v = new_values[i]

            # need a new block
            if m.any():
                nv = f(m, v, i)
            else:
                nv = v if inplace else v.copy()

            block = make_a_block(nv, [ref_loc])
            new_blocks.append(block)

        return new_blocks
