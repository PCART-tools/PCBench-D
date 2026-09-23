    def __init__(self, figure, width, height, dpi, vector_renderer,
                 raster_renderer_class=None,
                 bbox_inches_restore=None):
        """
        Parameters
        ----------
        figure : `matplotlib.figure.Figure`
            The figure instance.
        width : scalar
            The width of the canvas in logical units
        height : scalar
            The height of the canvas in logical units
        dpi : float
            The dpi of the canvas
        vector_renderer : `matplotlib.backend_bases.RendererBase`
            An instance of a subclass of
            `~matplotlib.backend_bases.RendererBase` that will be used for the
            vector drawing.
        raster_renderer_class : `matplotlib.backend_bases.RendererBase`
            The renderer class to use for the raster drawing.  If not provided,
            this will use the Agg backend (which is currently the only viable
            option anyway.)

        """
        if raster_renderer_class is None:
            raster_renderer_class = RendererAgg

        self._raster_renderer_class = raster_renderer_class
        self._width = width
        self._height = height
        self.dpi = dpi

        self._vector_renderer = vector_renderer

        self._raster_renderer = None

        # A reference to the figure is needed as we need to change
        # the figure dpi before and after the rasterization. Although
        # this looks ugly, I couldn't find a better solution. -JJL
        self.figure = figure
        self._figdpi = figure.get_dpi()

        self._bbox_inches_restore = bbox_inches_restore

        self._renderer = vector_renderer
