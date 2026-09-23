    def _astype(self, dtype, copy=False, raise_on_error=True, values=None,
                klass=None, mgr=None, **kwargs):
        if values is None:
            values = self.values
        values = values.astype(dtype, copy=copy)
        return self.make_block_same_class(values=values,
                                          placement=self.mgr_locs)
