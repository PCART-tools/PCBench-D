    def set_resample(self, v):
        """
        Set whether image resampling is used.

        Parameters
        ----------
        v : bool or None
            If None, use :rc:`image.resample` = True.
        """
        if v is None:
            v = rcParams['image.resample']
        self._resample = v
        self.stale = True
