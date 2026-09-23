    def __init__(self, ax, **kwargs):
        """
        kwargs are identical to those for AxesImage, except
        that 'nearest' and 'bilinear' are the only supported 'interpolation'
        options.
        """
        interp = kwargs.pop('interpolation', 'nearest')
        super(NonUniformImage, self).__init__(ax, **kwargs)
        self.set_interpolation(interp)
