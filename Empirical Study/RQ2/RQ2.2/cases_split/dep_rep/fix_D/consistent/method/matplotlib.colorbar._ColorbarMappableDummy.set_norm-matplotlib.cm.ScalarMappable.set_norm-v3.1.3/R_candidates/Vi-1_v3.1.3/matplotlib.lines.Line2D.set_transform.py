    def set_transform(self, t):
        """
        Set the Transformation instance used by this artist.

        Parameters
        ----------
        t : `matplotlib.transforms.Transform`
        """
        Artist.set_transform(self, t)
        self._invalidx = True
        self._invalidy = True
        self.stale = True
