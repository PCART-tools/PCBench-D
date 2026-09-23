    def _mesh(self):
        '''
        Return X,Y, the coordinate arrays for the colorbar pcolormesh.
        These are suitable for a vertical colorbar; swapping and
        transposition for a horizontal colorbar are done outside
        this function.
        '''
        # if boundaries and values are None, then we can go ahead and
        # scale this up for Auto tick location.  Otherwise we
        # want to keep normalized between 0 and 1 and use manual tick
        # locations.

        x = np.array([0.0, 1.0])
        if self.spacing == 'uniform':
            y = self._uniform_y(self._central_N())
        else:
            y = self._proportional_y()
        if self._use_auto_colorbar_locator():
            y = self.norm.inverse(y)
            x = self.norm.inverse(x)
        self._y = y
        X, Y = np.meshgrid(x, y)
        if self._use_auto_colorbar_locator():
            xmid = self.norm.inverse(0.5)
        else:
            xmid = 0.5
        if self._extend_lower() and not self.extendrect:
            X[0, :] = xmid
        if self._extend_upper() and not self.extendrect:
            X[-1, :] = xmid
        return X, Y
