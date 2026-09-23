    def set_resample(self, v):
        """
        Set whether or not image resampling is used.

        Parameters
        ----------
        v : bool
        """
        if v is None:
            v = rcParams['image.resample']
        self._resample = v
        self.stale = True
