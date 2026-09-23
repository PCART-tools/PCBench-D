    @_api.make_keyword_only("3.6", name="cmap")
    def __init__(self, ax,
                 x=None,
                 y=None,
                 A=None,
                 cmap=None,
                 norm=None,
                 **kwargs
                 ):
        """
        Parameters
        ----------
        ax : `~.axes.Axes`
            The axes the image will belong to.
        x, y : 1D array-like, optional
            Monotonic arrays of length N+1 and M+1, respectively, specifying
            rectangle boundaries.  If not given, will default to
            ``range(N + 1)`` and ``range(M + 1)``, respectively.
        A : array-like
            The data to be color-coded. The interpretation depends on the
            shape:

            - (M, N) `~numpy.ndarray` or masked array: values to be colormapped
            - (M, N, 3): RGB array
            - (M, N, 4): RGBA array

        cmap : str or `~matplotlib.colors.Colormap`, default: :rc:`image.cmap`
            The Colormap instance or registered colormap name used to map
            scalar data to colors.
        norm : str or `~matplotlib.colors.Normalize`
            Maps luminance to 0-1.
        **kwargs : `.Artist` properties
        """
        super().__init__(ax, norm=norm, cmap=cmap)
        self._internal_update(kwargs)
        if A is not None:
            self.set_data(x, y, A)
