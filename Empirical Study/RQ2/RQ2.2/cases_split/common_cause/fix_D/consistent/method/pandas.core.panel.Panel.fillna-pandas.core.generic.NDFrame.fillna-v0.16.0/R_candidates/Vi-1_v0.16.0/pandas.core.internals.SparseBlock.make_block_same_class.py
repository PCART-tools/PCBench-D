    def make_block_same_class(self, values, placement,
                              sparse_index=None, kind=None, dtype=None,
                              fill_value=None, copy=False, fastpath=True):
        """ return a new block """
        if dtype is None:
            dtype = self.dtype
        if fill_value is None:
            fill_value = self.values.fill_value

        # if not isinstance(values, SparseArray) and values.ndim != self.ndim:
        #     raise ValueError("ndim mismatch")

        if values.ndim == 2:
            nitems = values.shape[0]

            if nitems == 0:
                # kludgy, but SparseBlocks cannot handle slices, where the
                # output is 0-item, so let's convert it to a dense block: it
                # won't take space since there's 0 items, plus it will preserve
                # the dtype.
                return make_block(np.empty(values.shape, dtype=dtype),
                                  placement, fastpath=True,)
            elif nitems > 1:
                raise ValueError("Only 1-item 2d sparse blocks are supported")
            else:
                values = values.reshape(values.shape[1])

        new_values = SparseArray(values, sparse_index=sparse_index,
                                 kind=kind or self.kind, dtype=dtype,
                                 fill_value=fill_value, copy=copy)
        return make_block(new_values, ndim=self.ndim,
                          fastpath=fastpath, placement=placement)
