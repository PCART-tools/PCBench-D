    def set_transform(self, t):
        """
        Set the :class:`matplotlib.transforms.Transform` instance used
        by this artist.

        Parameters
        ----------
        t : matplotlib.transforms.Transform
        """
        Text.set_transform(self, t)
        self.dashline.set_transform(t)
        self.stale = True
