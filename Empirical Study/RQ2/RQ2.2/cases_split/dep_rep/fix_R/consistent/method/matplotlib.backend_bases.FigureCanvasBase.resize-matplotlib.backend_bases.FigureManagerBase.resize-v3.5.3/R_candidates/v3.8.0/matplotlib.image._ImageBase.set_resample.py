    def set_resample(self, v):
        """
        Set whether image resampling is used.

        Parameters
        ----------
        v : bool or None
            If None, use :rc:`image.resample`.
        """
        v = mpl._val_or_rc(v, 'image.resample')
        self._resample = v
        self.stale = True
