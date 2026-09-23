    def __init__(self, ax, *, interpolation='nearest', **kwargs):
        """
        kwargs are identical to those for AxesImage, except
        that 'nearest' and 'bilinear' are the only supported 'interpolation'
        options.
        """
        super().__init__(ax, **kwargs)
        self.set_interpolation(interpolation)
