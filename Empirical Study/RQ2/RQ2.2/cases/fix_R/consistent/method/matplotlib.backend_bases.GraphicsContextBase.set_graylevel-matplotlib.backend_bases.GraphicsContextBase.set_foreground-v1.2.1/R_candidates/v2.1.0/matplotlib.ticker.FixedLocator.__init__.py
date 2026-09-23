    def __init__(self, locs, nbins=None):
        self.locs = np.asarray(locs)
        self.nbins = nbins
        if self.nbins is not None:
            self.nbins = max(self.nbins, 2)
