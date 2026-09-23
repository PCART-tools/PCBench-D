    def __init__(self, gamma, vmin=None, vmax=None, clip=False):
        Normalize.__init__(self, vmin, vmax, clip)
        self.gamma = gamma
