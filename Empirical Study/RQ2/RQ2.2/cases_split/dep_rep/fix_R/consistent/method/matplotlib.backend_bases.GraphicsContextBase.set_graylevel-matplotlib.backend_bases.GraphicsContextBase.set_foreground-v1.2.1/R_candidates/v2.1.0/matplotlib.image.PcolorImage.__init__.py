    def __init__(self, ax,
                 x=None,
                 y=None,
                 A=None,
                 cmap=None,
                 norm=None,
                 **kwargs
                 ):
        """
        cmap defaults to its rc setting

        cmap is a colors.Colormap instance
        norm is a colors.Normalize instance to map luminance to 0-1

        Additional kwargs are matplotlib.artist properties
        """
        super(PcolorImage, self).__init__(ax, norm=norm, cmap=cmap)
        self.update(kwargs)
        if A is not None:
            self.set_data(x, y, A)
