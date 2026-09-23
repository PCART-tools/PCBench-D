    def __init__(self, colorbar, n=None):
        """
        This ticker needs to know the *colorbar* so that it can access
        its *vmin* and *vmax*.
        """
        self._colorbar = colorbar
        self.ndivs = n
        super().__init__(n=None)
