    def _mesh(self):
        '''
        Return X,Y, the coordinate arrays for the colorbar pcolormesh.
        These are suitable for a vertical colorbar; swapping and
        transposition for a horizontal colorbar are done outside
        this function.
        '''
        x = np.array([0.0, 1.0])
        if self.spacing == 'uniform':
            y = self._uniform_y(self._central_N())
        else:
            y = self._proportional_y()
        self._y = y
        X, Y = np.meshgrid(x, y)
        if self._extend_lower() and not self.extendrect:
            X[0, :] = 0.5
        if self._extend_upper() and not self.extendrect:
            X[-1, :] = 0.5
        return X, Y
