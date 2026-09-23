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
        norm = copy.copy(self.norm)
        norm.vmin = self.vmin
        norm.vmax = self.vmax
        x = np.array([0.0, 1.0])
        if self.spacing == 'uniform':
            n_boundaries_no_extensions = len(self._boundaries[self._inside])
            y = self._uniform_y(n_boundaries_no_extensions)
        else:
            y = self._proportional_y()
        xmid = np.array([0.5])
        if self.__scale != 'manual':
            y = norm.inverse(y)
            x = norm.inverse(x)
            xmid = norm.inverse(xmid)
        else:
            # if a norm doesn't have a named scale, or
            # we are not using a norm
            dv = self.vmax - self.vmin
            x = x * dv + self.vmin
            y = y * dv + self.vmin
            xmid = xmid * dv + self.vmin
        self._y = y
        X, Y = np.meshgrid(x, y)
        if self._extend_lower() and not self.extendrect:
            X[0, :] = xmid
        if self._extend_upper() and not self.extendrect:
            X[-1, :] = xmid
        return (X, Y) if self.orientation == 'vertical' else (Y, X)
