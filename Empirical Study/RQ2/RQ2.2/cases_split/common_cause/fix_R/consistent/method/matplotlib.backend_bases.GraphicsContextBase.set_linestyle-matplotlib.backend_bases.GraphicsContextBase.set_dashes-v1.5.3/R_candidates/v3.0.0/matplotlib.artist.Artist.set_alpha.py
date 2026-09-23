    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : float
        """
        self._alpha = alpha
        self.pchanged()
        self.stale = True
