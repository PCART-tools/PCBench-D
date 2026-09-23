    def set_data(self, x, y, A):
        """
        Set the grid for the rectangle boundaries, and the data values.

        Parameters
        ----------
        x, y : 1D array-like, optional
            Monotonic arrays of length N+1 and M+1, respectively, specifying
            rectangle boundaries.  If not given, will default to
            ``range(N + 1)`` and ``range(M + 1)``, respectively.
        A : array-like
            The data to be color-coded. The interpretation depends on the
            shape:

            - (M, N) `~numpy.ndarray` or masked array: values to be colormapped
            - (M, N, 3): RGB array
            - (M, N, 4): RGBA array
        """
        A = cbook.safe_masked_invalid(A, copy=True)
        if x is None:
            x = np.arange(0, A.shape[1]+1, dtype=np.float64)
        else:
            x = np.array(x, np.float64).ravel()
        if y is None:
            y = np.arange(0, A.shape[0]+1, dtype=np.float64)
        else:
            y = np.array(y, np.float64).ravel()

        if A.shape[:2] != (y.size-1, x.size-1):
            raise ValueError(
                "Axes don't match array shape. Got %s, expected %s." %
                (A.shape[:2], (y.size - 1, x.size - 1)))
        if A.ndim not in [2, 3]:
            raise ValueError("A must be 2D or 3D")
        if A.ndim == 3:
            if A.shape[2] == 1:
                A = A.squeeze(axis=-1)
            elif A.shape[2] not in [3, 4]:
                raise ValueError("3D arrays must have RGB or RGBA as last dim")

        # For efficient cursor readout, ensure x and y are increasing.
        if x[-1] < x[0]:
            x = x[::-1]
            A = A[:, ::-1]
        if y[-1] < y[0]:
            y = y[::-1]
            A = A[::-1]

        self._A = A
        self._Ax = x
        self._Ay = y
        self._imcache = None
        self.stale = True
