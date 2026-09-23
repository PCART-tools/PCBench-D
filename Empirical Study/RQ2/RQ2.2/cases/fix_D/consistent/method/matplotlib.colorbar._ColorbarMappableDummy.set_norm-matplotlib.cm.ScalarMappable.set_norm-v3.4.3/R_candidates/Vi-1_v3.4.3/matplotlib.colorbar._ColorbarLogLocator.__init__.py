    def __init__(self, colorbar, *args, **kwargs):
        """
        This ticker needs to know the *colorbar* so that it can access
        its *vmin* and *vmax*.  Otherwise it is the same as
        `~.ticker.LogLocator`.  The ``*args`` and ``**kwargs`` are the
        same as `~.ticker.LogLocator`.
        """
        self._colorbar = colorbar
        super().__init__(*args, **kwargs)
