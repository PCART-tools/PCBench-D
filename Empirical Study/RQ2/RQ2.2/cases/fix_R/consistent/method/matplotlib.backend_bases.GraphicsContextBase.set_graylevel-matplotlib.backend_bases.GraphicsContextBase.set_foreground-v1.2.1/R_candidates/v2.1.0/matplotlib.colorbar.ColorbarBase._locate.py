    def _locate(self, x):
        '''
        Given a set of color data values, return their
        corresponding colorbar data coordinates.
        '''
        if isinstance(self.norm, (colors.NoNorm, colors.BoundaryNorm)):
            b = self._boundaries
            xn = x
        else:
            # Do calculations using normalized coordinates so
            # as to make the interpolation more accurate.
            b = self.norm(self._boundaries, clip=False).filled()
            xn = self.norm(x, clip=False).filled()

        # The rest is linear interpolation with extrapolation at ends.
        ii = np.searchsorted(b, xn)
        i0 = ii - 1
        itop = (ii == len(b))
        ibot = (ii == 0)
        i0[itop] -= 1
        ii[itop] -= 1
        i0[ibot] += 1
        ii[ibot] += 1

        db = np.take(b, ii) - np.take(b, i0)
        y = self._y
        dy = np.take(y, ii) - np.take(y, i0)
        z = np.take(y, i0) + (xn - np.take(b, i0)) * dy / db
        return z
