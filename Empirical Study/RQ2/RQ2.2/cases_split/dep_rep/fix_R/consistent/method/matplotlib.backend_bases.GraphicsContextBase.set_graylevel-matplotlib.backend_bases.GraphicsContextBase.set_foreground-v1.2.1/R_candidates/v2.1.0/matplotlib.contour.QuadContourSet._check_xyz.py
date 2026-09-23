    def _check_xyz(self, args, kwargs):
        """
        For functions like contour, check that the dimensions
        of the input arrays match; if x and y are 1D, convert
        them to 2D using meshgrid.

        Possible change: I think we should make and use an ArgumentError
        Exception class (here and elsewhere).
        """
        x, y = args[:2]
        kwargs = self.ax._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)
        x = self.ax.convert_xunits(x)
        y = self.ax.convert_yunits(y)

        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        z = ma.asarray(args[2], dtype=np.float64)

        if z.ndim != 2:
            raise TypeError("Input z must be a 2D array.")
        elif z.shape[0] < 2 or z.shape[1] < 2:
            raise TypeError("Input z must be at least a 2x2 array.")
        else:
            Ny, Nx = z.shape

        if x.ndim != y.ndim:
            raise TypeError("Number of dimensions of x and y should match.")

        if x.ndim == 1:

            nx, = x.shape
            ny, = y.shape

            if nx != Nx:
                raise TypeError("Length of x must be number of columns in z.")

            if ny != Ny:
                raise TypeError("Length of y must be number of rows in z.")

            x, y = np.meshgrid(x, y)

        elif x.ndim == 2:

            if x.shape != z.shape:
                raise TypeError("Shape of x does not match that of z: found "
                                "{0} instead of {1}.".format(x.shape, z.shape))

            if y.shape != z.shape:
                raise TypeError("Shape of y does not match that of z: found "
                                "{0} instead of {1}.".format(y.shape, z.shape))
        else:
            raise TypeError("Inputs x and y must be 1D or 2D.")

        return x, y, z
