    def make_block(self, values, placement=None, ndim=None, **kwargs):
        """
        Create a new block, with type inference propagate any values that are
        not specified
        """
        if placement is None:
            placement = self.mgr_locs
        if ndim is None:
            ndim = self.ndim

        return make_block(values, placement=placement, ndim=ndim, **kwargs)
