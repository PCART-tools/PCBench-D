    def __init__(self, ax, *, interpolation='nearest', **kwargs):
        """
        Parameters
        ----------
        interpolation : {'nearest', 'bilinear'}

        **kwargs
            All other keyword arguments are identical to those of `.AxesImage`.
        """
        super().__init__(ax, **kwargs)
        self.set_interpolation(interpolation)
