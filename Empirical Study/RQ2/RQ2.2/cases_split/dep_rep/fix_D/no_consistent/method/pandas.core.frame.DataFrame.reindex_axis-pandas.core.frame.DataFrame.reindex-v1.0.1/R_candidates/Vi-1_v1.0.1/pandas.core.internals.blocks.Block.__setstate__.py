    def __setstate__(self, state):
        self.mgr_locs = libinternals.BlockPlacement(state[0])
        self.values = state[1]
        self.ndim = self.values.ndim
