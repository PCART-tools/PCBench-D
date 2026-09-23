    def make_block_same_class(self, values, placement=None, fastpath=True,
                              **kwargs):
        """ Wrap given values in a block of same type as self. """
        if placement is None:
            placement = self.mgr_locs
        return make_block(values, placement=placement, klass=self.__class__,
                          fastpath=fastpath, **kwargs)
