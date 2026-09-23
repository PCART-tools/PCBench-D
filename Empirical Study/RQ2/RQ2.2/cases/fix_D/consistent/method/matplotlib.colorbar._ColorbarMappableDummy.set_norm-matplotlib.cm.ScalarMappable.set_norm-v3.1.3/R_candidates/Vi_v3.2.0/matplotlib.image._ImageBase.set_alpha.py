    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : float
        """
        if alpha is not None and not isinstance(alpha, Number):
            alpha = np.asarray(alpha)
            if alpha.ndim != 2:
                raise TypeError('alpha must be a float, two-dimensional '
                                'array, or None')
        self._alpha = alpha
        self.pchanged()
        self.stale = True
        self._imcache = None
