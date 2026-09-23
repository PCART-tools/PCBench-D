    def __init__(self, adjust_compatible, colorbar_gridspec, **kwargs):
        self._adjust_compatible = adjust_compatible
        self._colorbar_gridspec = colorbar_gridspec
        super().__init__(**kwargs)
