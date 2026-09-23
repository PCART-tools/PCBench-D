    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on
        all backends

        ACCEPTS: float
        """
        martist.Artist.set_alpha(self, alpha)
        self._imcache = None
