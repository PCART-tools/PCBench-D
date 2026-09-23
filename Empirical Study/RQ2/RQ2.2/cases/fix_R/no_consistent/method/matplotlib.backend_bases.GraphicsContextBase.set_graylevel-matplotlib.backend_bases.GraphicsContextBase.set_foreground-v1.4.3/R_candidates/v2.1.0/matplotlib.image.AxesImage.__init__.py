    def __init__(self, ax,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
                 extent=None,
                 filternorm=1,
                 filterrad=4.0,
                 resample=False,
                 **kwargs
                 ):

        """
        interpolation and cmap default to their rc settings

        cmap is a colors.Colormap instance
        norm is a colors.Normalize instance to map luminance to 0-1

        extent is data axes (left, right, bottom, top) for making image plots
        registered with data plots.  Default is to label the pixel
        centers with the zero-based row and column indices.

        Additional kwargs are matplotlib.artist properties

        """

        self._extent = extent

        super(AxesImage, self).__init__(
            ax,
            cmap=cmap,
            norm=norm,
            interpolation=interpolation,
            origin=origin,
            filternorm=filternorm,
            filterrad=filterrad,
            resample=resample,
            **kwargs
        )
