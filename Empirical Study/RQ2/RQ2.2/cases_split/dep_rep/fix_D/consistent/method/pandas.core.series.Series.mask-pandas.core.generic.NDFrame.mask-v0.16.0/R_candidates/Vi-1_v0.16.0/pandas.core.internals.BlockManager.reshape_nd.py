    def reshape_nd(self, axes, **kwargs):
        """ a 2d-nd reshape operation on a BlockManager """
        return self.apply('reshape_nd', axes=axes, **kwargs)
