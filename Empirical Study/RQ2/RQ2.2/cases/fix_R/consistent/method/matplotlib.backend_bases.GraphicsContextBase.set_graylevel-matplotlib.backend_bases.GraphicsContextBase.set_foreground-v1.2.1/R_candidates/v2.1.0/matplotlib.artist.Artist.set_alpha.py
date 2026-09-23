    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on
        all backends.

        ACCEPTS: float (0.0 transparent through 1.0 opaque)
        """
        self._alpha = alpha
        self.pchanged()
        self.stale = True
