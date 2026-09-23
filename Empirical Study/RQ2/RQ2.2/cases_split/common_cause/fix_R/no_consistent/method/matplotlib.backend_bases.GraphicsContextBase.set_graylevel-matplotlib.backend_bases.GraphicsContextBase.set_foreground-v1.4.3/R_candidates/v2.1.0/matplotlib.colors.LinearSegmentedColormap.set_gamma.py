    def set_gamma(self, gamma):
        """
        Set a new gamma value and regenerate color map.
        """
        self._gamma = gamma
        self._init()
