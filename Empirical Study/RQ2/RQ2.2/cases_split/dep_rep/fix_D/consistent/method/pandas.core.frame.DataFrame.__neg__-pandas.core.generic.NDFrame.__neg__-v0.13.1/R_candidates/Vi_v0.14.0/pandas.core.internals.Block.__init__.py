    def __init__(self, values, placement, ndim=None, fastpath=False):
        if ndim is None:
            ndim = values.ndim
        elif values.ndim != ndim:
            raise ValueError('Wrong number of dimensions')
        self.ndim = ndim

        self.mgr_locs = placement
        self.values = values

        if len(self.mgr_locs) != len(self.values):
            raise ValueError('Wrong number of items passed %d,'
                             ' placement implies %d' % (
                                 len(self.values), len(self.mgr_locs)))
