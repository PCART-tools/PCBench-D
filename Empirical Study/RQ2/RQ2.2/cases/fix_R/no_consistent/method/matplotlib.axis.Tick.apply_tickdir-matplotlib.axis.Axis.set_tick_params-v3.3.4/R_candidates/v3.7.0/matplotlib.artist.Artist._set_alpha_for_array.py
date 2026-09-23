    def _set_alpha_for_array(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : array-like or scalar or None
            All values must be within the 0-1 range, inclusive.
            Masked values and nans are not supported.
        """
        if isinstance(alpha, str):
            raise TypeError("alpha must be numeric or None, not a string")
        if not np.iterable(alpha):
            Artist.set_alpha(self, alpha)
            return
        alpha = np.asarray(alpha)
        if not (0 <= alpha.min() and alpha.max() <= 1):
            raise ValueError('alpha must be between 0 and 1, inclusive, '
                             f'but min is {alpha.min()}, max is {alpha.max()}')
        self._alpha = alpha
        self.pchanged()
        self.stale = True
