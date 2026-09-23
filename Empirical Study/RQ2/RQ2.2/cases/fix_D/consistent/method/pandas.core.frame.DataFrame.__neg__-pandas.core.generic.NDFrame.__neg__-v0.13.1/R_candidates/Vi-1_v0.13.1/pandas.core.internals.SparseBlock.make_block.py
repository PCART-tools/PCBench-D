    def make_block(self, values, items=None, ref_items=None, sparse_index=None,
                   kind=None, dtype=None, fill_value=None, copy=False,
                   fastpath=True):
        """ return a new block """
        if dtype is None:
            dtype = self.dtype
        if fill_value is None:
            fill_value = self.fill_value
        if items is None:
            items = self.items
        if ref_items is None:
            ref_items = self.ref_items
        new_values = SparseArray(values, sparse_index=sparse_index,
                                 kind=kind or self.kind, dtype=dtype,
                                 fill_value=fill_value, copy=copy)
        return make_block(new_values, items, ref_items, ndim=self.ndim,
                          fastpath=fastpath)
