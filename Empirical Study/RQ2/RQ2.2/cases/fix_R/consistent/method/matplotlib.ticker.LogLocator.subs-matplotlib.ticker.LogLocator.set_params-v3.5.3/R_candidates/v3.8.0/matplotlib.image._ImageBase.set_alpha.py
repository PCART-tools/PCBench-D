    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : float or 2D array-like or None
        """
        martist.Artist._set_alpha_for_array(self, alpha)
        if np.ndim(alpha) not in (0, 2):
            raise TypeError('alpha must be a float, two-dimensional '
                            'array, or None')
        self._imcache = None
