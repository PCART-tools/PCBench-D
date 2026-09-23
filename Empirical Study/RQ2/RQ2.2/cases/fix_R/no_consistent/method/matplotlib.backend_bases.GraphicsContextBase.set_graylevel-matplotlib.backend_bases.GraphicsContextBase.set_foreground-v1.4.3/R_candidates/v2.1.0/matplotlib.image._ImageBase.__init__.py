    def __init__(self, ax,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
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
        martist.Artist.__init__(self)
        cm.ScalarMappable.__init__(self, norm, cmap)
        self._mouseover = True
        if origin is None:
            origin = rcParams['image.origin']
        self.origin = origin
        self.set_filternorm(filternorm)
        self.set_filterrad(filterrad)
        self.set_interpolation(interpolation)
        self.set_resample(resample)
        self.axes = ax

        self._imcache = None

        self.update(kwargs)
