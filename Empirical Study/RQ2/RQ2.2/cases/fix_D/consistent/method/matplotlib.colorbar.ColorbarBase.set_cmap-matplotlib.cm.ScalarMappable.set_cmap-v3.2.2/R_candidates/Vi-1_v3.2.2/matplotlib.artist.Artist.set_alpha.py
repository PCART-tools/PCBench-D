    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : float or None
        """
        if alpha is not None and not isinstance(alpha, Number):
            raise TypeError('alpha must be a float or None')
        self._alpha = alpha
        self.pchanged()
        self.stale = True
