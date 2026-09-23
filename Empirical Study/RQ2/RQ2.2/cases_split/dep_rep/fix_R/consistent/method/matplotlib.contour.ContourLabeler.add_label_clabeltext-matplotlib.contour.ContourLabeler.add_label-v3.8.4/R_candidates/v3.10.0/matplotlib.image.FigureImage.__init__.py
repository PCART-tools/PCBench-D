    def __init__(self, fig,
                 *,
                 cmap=None,
                 norm=None,
                 colorizer=None,
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
            colorizer=colorizer,
            origin=origin
        )
        self.set_figure(fig)
        self.ox = offsetx
        self.oy = offsety
        self._internal_update(kwargs)
        self.magnification = 1.0
