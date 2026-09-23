    def __init__(self, colorbar):
        """
        This ticker needs to know the *colorbar* so that it can access
        its *vmin* and *vmax*.  Otherwise it is the same as
        `~.ticker.AutoLocator`.
        """

        self._colorbar = colorbar
        nbins = 'auto'
        steps = [1, 2, 2.5, 5, 10]
        ticker.MaxNLocator.__init__(self, nbins=nbins, steps=steps)
