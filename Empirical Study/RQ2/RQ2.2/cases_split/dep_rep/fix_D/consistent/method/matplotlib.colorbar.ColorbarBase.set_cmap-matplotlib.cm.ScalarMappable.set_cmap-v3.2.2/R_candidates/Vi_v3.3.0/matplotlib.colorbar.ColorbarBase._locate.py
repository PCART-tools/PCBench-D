    def _locate(self, x):
        """
        Given a set of color data values, return their
        corresponding colorbar data coordinates.
        """
        if isinstance(self.norm, (colors.NoNorm, colors.BoundaryNorm)):
            b = self._boundaries
            xn = x
        else:
            # Do calculations using normalized coordinates so
            # as to make the interpolation more accurate.
            b = self.norm(self._boundaries, clip=False).filled()
            xn = self.norm(x, clip=False).filled()

        bunique = b
        yunique = self._y
        # trim extra b values at beginning and end if they are
        # not unique.  These are here for extended colorbars, and are not
        # wanted for the interpolation.
        if b[0] == b[1]:
            bunique = bunique[1:]
            yunique = yunique[1:]
        if b[-1] == b[-2]:
            bunique = bunique[:-1]
            yunique = yunique[:-1]

        z = np.interp(xn, bunique, yunique)
        return z
