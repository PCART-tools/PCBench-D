    def __init__(self, axes):
        self._ax = axes
        super().__init__(axes, 'colorbar', mpath.Path(np.empty((0, 2))))
        mpatches.Patch.set_transform(self, axes.transAxes)
