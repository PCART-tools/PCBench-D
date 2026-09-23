    def set_gamma(self, gamma):
        """Set a new gamma value and regenerate colormap."""
        self._gamma = gamma
        self._init()
