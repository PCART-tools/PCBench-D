    def __init__(self, norm=None, cmap=None):
        """
        Parameters
        ----------
        norm : `.Normalize` (or subclass thereof) or str or None
            The normalizing object which scales data, typically into the
            interval ``[0, 1]``.
            If a `str`, a `.Normalize` subclass is dynamically generated based
            on the scale with the corresponding name.
            If *None*, *norm* defaults to a *colors.Normalize* object which
            initializes its scaling based on the first data processed.
        cmap : str or `~matplotlib.colors.Colormap`
            The colormap used to map normalized data values to RGBA colors.
        """
        self._A = None
        self._norm = None  # So that the setter knows we're initializing.
        self.set_norm(norm)  # The Normalize instance of this ScalarMappable.
        self.cmap = None  # So that the setter knows we're initializing.
        self.set_cmap(cmap)  # The Colormap instance of this ScalarMappable.
        #: The last colorbar associated with this ScalarMappable. May be None.
        self.colorbar = None
        self.callbacks = cbook.CallbackRegistry(signals=["changed"])
