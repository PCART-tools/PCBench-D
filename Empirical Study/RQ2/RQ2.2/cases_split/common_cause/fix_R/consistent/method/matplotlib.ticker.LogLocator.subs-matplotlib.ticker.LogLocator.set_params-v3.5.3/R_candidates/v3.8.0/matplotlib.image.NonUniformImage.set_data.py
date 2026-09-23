    def set_data(self, x, y, A):
        """
        Set the grid for the pixel centers, and the pixel values.

        Parameters
        ----------
        x, y : 1D array-like
            Monotonic arrays of shapes (N,) and (M,), respectively, specifying
            pixel centers.
        A : array-like
            (M, N) `~numpy.ndarray` or masked array of values to be
            colormapped, or (M, N, 3) RGB array, or (M, N, 4) RGBA array.
        """
        A = self._normalize_image_array(A)
        x = np.array(x, np.float32)
        y = np.array(y, np.float32)
        if not (x.ndim == y.ndim == 1 and A.shape[:2] == y.shape + x.shape):
            raise TypeError("Axes don't match array shape")
        self._A = A
        self._Ax = x
        self._Ay = y
        self._imcache = None
        self.stale = True
