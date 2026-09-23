    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : scalar or None
            *alpha* must be within the 0-1 range, inclusive.
        """
        if alpha is not None and not isinstance(alpha, Number):
            raise TypeError(
                f'alpha must be numeric or None, not {type(alpha)}')
        if alpha is not None and not (0 <= alpha <= 1):
            raise ValueError(f'alpha ({alpha}) is outside 0-1 range')
        self._alpha = alpha
        self.pchanged()
        self.stale = True
