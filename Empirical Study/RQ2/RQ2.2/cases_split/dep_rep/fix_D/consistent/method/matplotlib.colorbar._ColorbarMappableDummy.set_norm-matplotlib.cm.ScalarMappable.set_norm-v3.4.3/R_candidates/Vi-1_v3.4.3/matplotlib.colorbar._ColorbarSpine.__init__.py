    def __init__(self, axes):
        super().__init__(axes, 'colorbar',
                         mpath.Path(np.empty((0, 2)), closed=True))
