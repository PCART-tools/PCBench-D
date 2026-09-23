    def set_transform(self, t):
        """
        set the Transformation instance used by this artist

        ACCEPTS: a :class:`matplotlib.transforms.Transform` instance
        """
        Artist.set_transform(self, t)
        self._invalidx = True
        self._invalidy = True
        self.stale = True
