    def set_transform(self, t):
        """
        Set the artist transform.

        Parameters
        ----------
        t : `~matplotlib.transforms.Transform`
        """
        self._transform = t
        self._transformSet = True
        self.pchanged()
        self.stale = True
