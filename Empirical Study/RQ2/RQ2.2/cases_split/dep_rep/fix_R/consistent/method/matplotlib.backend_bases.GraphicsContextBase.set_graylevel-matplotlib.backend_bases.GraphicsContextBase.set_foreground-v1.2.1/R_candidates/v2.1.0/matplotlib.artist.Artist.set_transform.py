    def set_transform(self, t):
        """
        Set the :class:`~matplotlib.transforms.Transform` instance
        used by this artist.

        ACCEPTS: :class:`~matplotlib.transforms.Transform` instance
        """
        self._transform = t
        self._transformSet = True
        self.pchanged()
        self.stale = True
