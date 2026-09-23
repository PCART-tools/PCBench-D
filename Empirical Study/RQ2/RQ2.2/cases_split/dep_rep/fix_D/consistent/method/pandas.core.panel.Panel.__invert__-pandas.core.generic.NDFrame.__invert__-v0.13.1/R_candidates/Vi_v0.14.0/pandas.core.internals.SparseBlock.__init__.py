    def __init__(self, values, placement,
                 ndim=None, fastpath=False,):

        # kludgetastic
        if ndim is None:
            if len(placement) != 1:
                ndim = 1
            else:
                ndim = 2
        self.ndim = ndim

        self.mgr_locs = placement

        if not isinstance(values, SparseArray):
            raise TypeError("values must be SparseArray")

        self.values = values
