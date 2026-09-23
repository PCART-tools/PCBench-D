    def _mesh(self):
        """
        Return the coordinate arrays for the colorbar pcolormesh/patches.

        These are scaled between vmin and vmax, and already handle colorbar
        orientation.
        """
        # copy the norm and change the vmin and vmax to the vmin and
        # vmax of the colorbar, not the norm.  This allows the situation
        # where the colormap has a narrower range than the colorbar, to
        # accommodate extra contours:
        norm = copy.deepcopy(self.norm)
        norm.vmin = self.vmin
        norm.vmax = self.vmax
        x = np.array([0.0, 1.0])
        y, extendlen = self._proportional_y()
        # invert:
        if (isinstance(norm, (colors.BoundaryNorm, colors.NoNorm)) or
                (self.__scale == 'manual')):
            # if a norm doesn't have a named scale, or we are not using a norm:
            dv = self.vmax - self.vmin
            y = y * dv + self.vmin
        else:
            y = norm.inverse(y)
        self._y = y
        X, Y = np.meshgrid(x, y)
        if self.orientation == 'vertical':
            return (X, Y, extendlen)
        else:
            return (Y, X, extendlen)
