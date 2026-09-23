    def make_block(self, values, placement=None):
        """
        Create a new block, with type inference propagate any values that are
        not specified
        """
        if placement is None:
            placement = self.mgr_locs

        return make_block(values, placement=placement, ndim=self.ndim)
