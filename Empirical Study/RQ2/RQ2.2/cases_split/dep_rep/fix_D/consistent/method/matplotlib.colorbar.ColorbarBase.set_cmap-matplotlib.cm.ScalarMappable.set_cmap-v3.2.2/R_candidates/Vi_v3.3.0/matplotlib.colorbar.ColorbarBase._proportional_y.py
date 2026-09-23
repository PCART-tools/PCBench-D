    def _proportional_y(self):
        """
        Return colorbar data coordinates for the boundaries of
        a proportional colorbar.
        """
        if isinstance(self.norm, colors.BoundaryNorm):
            y = (self._boundaries - self._boundaries[0])
            y = y / (self._boundaries[-1] - self._boundaries[0])
        else:
            y = self.norm(self._boundaries.copy())
            y = np.ma.filled(y, np.nan)
        if self.extend == 'min':
            # Exclude leftmost interval of y.
            clen = y[-1] - y[1]
            automin = (y[2] - y[1]) / clen
            automax = (y[-1] - y[-2]) / clen
        elif self.extend == 'max':
            # Exclude rightmost interval in y.
            clen = y[-2] - y[0]
            automin = (y[1] - y[0]) / clen
            automax = (y[-2] - y[-3]) / clen
        elif self.extend == 'both':
            # Exclude leftmost and rightmost intervals in y.
            clen = y[-2] - y[1]
            automin = (y[2] - y[1]) / clen
            automax = (y[-2] - y[-3]) / clen
        if self.extend in ('both', 'min', 'max'):
            extendlength = self._get_extension_lengths(self.extendfrac,
                                                       automin, automax,
                                                       default=0.05)
        if self.extend in ('both', 'min'):
            y[0] = 0. - extendlength[0]
        if self.extend in ('both', 'max'):
            y[-1] = 1. + extendlength[1]
        yi = y[self._inside]
        norm = colors.Normalize(yi[0], yi[-1])
        y[self._inside] = np.ma.filled(norm(yi), np.nan)
        return y
