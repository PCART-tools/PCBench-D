    def make_block_same_class(self, values, placement=None, ndim=None):
        """ Wrap given values in a block of same type as self. """
        if placement is None:
            placement = self.mgr_locs
        if ndim is None:
            ndim = self.ndim
        return make_block(values, placement=placement, ndim=ndim, klass=type(self))
