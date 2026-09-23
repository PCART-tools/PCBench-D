    def set_graylevel(self, frac):
        """
        Set the foreground color to be a gray level with *frac*
        """
        # When removing, remember to remove all overrides in subclasses.
        msg = ("set_graylevel is deprecated for removal in 1.6; "
                "you can achieve the same result by using "
                "set_foreground((frac, frac, frac))")
        warnings.warn(msg, mplDeprecation)
        self._rgb = (frac, frac, frac, self._alpha)
