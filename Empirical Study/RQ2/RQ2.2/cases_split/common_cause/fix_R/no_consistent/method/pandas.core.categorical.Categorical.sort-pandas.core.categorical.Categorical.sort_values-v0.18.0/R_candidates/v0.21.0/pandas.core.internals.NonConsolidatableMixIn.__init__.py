    def __init__(self, values, placement, ndim=None, fastpath=False, **kwargs):

        # Placement must be converted to BlockPlacement via property setter
        # before ndim logic, because placement may be a slice which doesn't
        # have a length.
        self.mgr_locs = placement

        # kludgetastic
        if ndim is None:
            if len(self.mgr_locs) != 1:
                ndim = 1
            else:
                ndim = 2
        self.ndim = ndim

        if not isinstance(values, self._holder):
            raise TypeError("values must be {0}".format(self._holder.__name__))

        self.values = values
