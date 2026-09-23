    def __init__(self, norm=None, cmap=None):
        r"""

        Parameters
        ----------
        norm : :class:`matplotlib.colors.Normalize` instance
            The normalizing object which scales data, typically into the
            interval ``[0, 1]``.
            If *None*, *norm* defaults to a *colors.Normalize* object which
            initializes its scaling based on the first data processed.
        cmap : str or :class:`~matplotlib.colors.Colormap` instance
            The colormap used to map normalized data values to RGBA colors.
        """

        self.callbacksSM = cbook.CallbackRegistry()

        if cmap is None:
            cmap = get_cmap()
        if norm is None:
            norm = colors.Normalize()

        self._A = None
        #: The Normalization instance of this ScalarMappable.
        self.norm = norm
        #: The Colormap instance of this ScalarMappable.
        self.cmap = get_cmap(cmap)
        #: The last colorbar associated with this ScalarMappable. May be None.
        self.colorbar = None
        self.update_dict = {'array': False}
