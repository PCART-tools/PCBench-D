    def _resample(self, lutsize):
        """
        Return a new color map with *lutsize* entries.
        """
        colors = self(np.linspace(0, 1, lutsize))
        return ListedColormap(colors, name=self.name)
