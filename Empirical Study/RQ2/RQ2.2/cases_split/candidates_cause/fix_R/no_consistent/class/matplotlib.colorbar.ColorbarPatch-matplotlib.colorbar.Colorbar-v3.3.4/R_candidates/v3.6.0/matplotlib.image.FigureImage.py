class FigureImage(_ImageBase):
    """An image attached to a figure."""

    zorder = 0

    _interpolation = 'nearest'

    @_api.make_keyword_only("3.6", name="cmap")
    def __init__(self, fig,
                 cmap=None,
                 norm=None,
                 offsetx=0,
                 offsety=0,
                 origin=None,
                 **kwargs
                 ):
        """
        cmap is a colors.Colormap instance
        norm is a colors.Normalize instance to map luminance to 0-1

        kwargs are an optional list of Artist keyword args
        """
        super().__init__(
            None,
            norm=norm,
            cmap=cmap,
            origin=origin
        )
        self.figure = fig
        self.ox = offsetx
        self.oy = offsety
        self._internal_update(kwargs)
        self.magnification = 1.0

    def get_extent(self):
        """Return the image extent as tuple (left, right, bottom, top)."""
        numrows, numcols = self.get_size()
        return (-0.5 + self.ox, numcols-0.5 + self.ox,
                -0.5 + self.oy, numrows-0.5 + self.oy)

    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        fac = renderer.dpi/self.figure.dpi
        # fac here is to account for pdf, eps, svg backends where
        # figure.dpi is set to 72.  This means we need to scale the
        # image (using magnification) and offset it appropriately.
        bbox = Bbox([[self.ox/fac, self.oy/fac],
                     [(self.ox/fac + self._A.shape[1]),
                     (self.oy/fac + self._A.shape[0])]])
        width, height = self.figure.get_size_inches()
        width *= renderer.dpi
        height *= renderer.dpi
        clip = Bbox([[0, 0], [width, height]])
        return self._make_image(
            self._A, bbox, bbox, clip, magnification=magnification / fac,
            unsampled=unsampled, round_to_pixel_border=False)

    def set_data(self, A):
        """Set the image array."""
        cm.ScalarMappable.set_array(self, A)
        self.stale = True
