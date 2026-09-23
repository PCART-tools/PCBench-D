    def set_resample(self, v):
        """
        Set whether image resampling is used.

        Parameters
        ----------
        v : bool or None
            If None, use :rc:`image.resample`.
        """
        if v is None:
            v = mpl.rcParams['image.resample']
        self._resample = v
        self.stale = True
