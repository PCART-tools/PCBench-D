    def __init__(self, patch, N=256, shape='square', origin=(0, 0),
                 name='segmented bivariate colormap'):
        _api.check_shape((None, None, 3), patch=patch)
        self.patch = patch
        super().__init__(N, N, shape, origin, name=name)
