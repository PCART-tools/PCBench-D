    def __init__(self, locs, nbins=None):
        self.locs = np.asarray(locs)
        self.nbins = max(nbins, 2) if nbins is not None else None
