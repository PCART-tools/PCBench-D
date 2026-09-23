    def set_graylevel(self, frac):
        """
        Set the foreground color to be a gray level with *frac*
        """
        self._orig_color = frac
        self._rgb = (frac, frac, frac, self._alpha)
