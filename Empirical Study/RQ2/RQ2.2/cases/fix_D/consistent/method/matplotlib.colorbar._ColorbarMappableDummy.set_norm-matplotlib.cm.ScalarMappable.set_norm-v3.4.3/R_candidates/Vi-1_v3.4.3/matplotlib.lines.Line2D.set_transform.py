    def set_transform(self, t):
        """
        Set the Transformation instance used by this artist.

        Parameters
        ----------
        t : `matplotlib.transforms.Transform`
        """
        super().set_transform(t)
        self._invalidx = True
        self._invalidy = True
        self.stale = True
