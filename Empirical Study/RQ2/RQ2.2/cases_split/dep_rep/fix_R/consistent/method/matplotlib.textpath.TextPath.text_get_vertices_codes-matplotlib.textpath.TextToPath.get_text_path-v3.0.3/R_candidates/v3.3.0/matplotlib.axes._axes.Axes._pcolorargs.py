    @staticmethod
    def _pcolorargs(funcname, *args, shading='flat'):
        # - create X and Y if not present;
        # - reshape X and Y as needed if they are 1-D;
        # - check for proper sizes based on `shading` kwarg;
        # - reset shading if shading='auto' to flat or nearest
        #   depending on size;

        if len(args) == 1:
            C = np.asanyarray(args[0])
            nrows, ncols = C.shape
            if shading in ['gouraud', 'nearest']:
                X, Y = np.meshgrid(np.arange(ncols), np.arange(nrows))
            else:
                X, Y = np.meshgrid(np.arange(ncols + 1), np.arange(nrows + 1))
                shading = 'flat'
            C = cbook.safe_masked_invalid(C)
            return X, Y, C, shading

        if len(args) == 3:
            # Check x and y for bad data...
            C = np.asanyarray(args[2])
            X, Y = [cbook.safe_masked_invalid(a) for a in args[:2]]
            if funcname == 'pcolormesh':
                if np.ma.is_masked(X) or np.ma.is_masked(Y):
                    raise ValueError(
                        'x and y arguments to pcolormesh cannot have '
                        'non-finite values or be of type '
                        'numpy.ma.core.MaskedArray with masked values')
                # safe_masked_invalid() returns an ndarray for dtypes other
                # than floating point.
                if isinstance(X, np.ma.core.MaskedArray):
                    X = X.data  # strip mask as downstream doesn't like it...
                if isinstance(Y, np.ma.core.MaskedArray):
                    Y = Y.data
            nrows, ncols = C.shape
        else:
            raise TypeError(f'{funcname}() takes 1 or 3 positional arguments '
                            f'but {len(args)} were given')

        Nx = X.shape[-1]
        Ny = Y.shape[0]
        if X.ndim != 2 or X.shape[0] == 1:
            x = X.reshape(1, Nx)
            X = x.repeat(Ny, axis=0)
        if Y.ndim != 2 or Y.shape[1] == 1:
            y = Y.reshape(Ny, 1)
            Y = y.repeat(Nx, axis=1)
        if X.shape != Y.shape:
            raise TypeError(
                'Incompatible X, Y inputs to %s; see help(%s)' % (
                funcname, funcname))

        if shading == 'auto':
            if ncols == Nx and nrows == Ny:
                shading = 'nearest'
            else:
                shading = 'flat'

        if shading == 'flat':
            if not (ncols in (Nx, Nx - 1) and nrows in (Ny, Ny - 1)):
                raise TypeError('Dimensions of C %s are incompatible with'
                                ' X (%d) and/or Y (%d); see help(%s)' % (
                                    C.shape, Nx, Ny, funcname))
            if (ncols == Nx or nrows == Ny):
                cbook.warn_deprecated(
                    "3.3", message="shading='flat' when X and Y have the same "
                    "dimensions as C is deprecated since %(since)s.  Either "
                    "specify the corners of the quadrilaterals with X and Y, "
                    "or pass shading='auto', 'nearest' or 'gouraud', or set "
                    "rcParams['pcolor.shading'].  This will become an error "
                    "%(removal)s.")
            C = C[:Ny - 1, :Nx - 1]
        else:    # ['nearest', 'gouraud']:
            if (Nx, Ny) != (ncols, nrows):
                raise TypeError('Dimensions of C %s are incompatible with'
                                ' X (%d) and/or Y (%d); see help(%s)' % (
                                    C.shape, Nx, Ny, funcname))
            if shading in ['nearest', 'auto']:
                # grid is specified at the center, so define corners
                # at the midpoints between the grid centers and then use the
                # flat algorithm.
                def _interp_grid(X):
                    # helper for below
                    if np.shape(X)[1] > 1:
                        dX = np.diff(X, axis=1)/2.
                        X = np.hstack((X[:, [0]] - dX[:, [0]],
                                       X[:, :-1] + dX,
                                       X[:, [-1]] + dX[:, [-1]]))
                    else:
                        # This is just degenerate, but we can't reliably guess
                        # a dX if there is just one value.
                        X = np.hstack((X, X))
                    return X

                if ncols == Nx:
                    X = _interp_grid(X)
                    Y = _interp_grid(Y)
                if nrows == Ny:
                    X = _interp_grid(X.T).T
                    Y = _interp_grid(Y.T).T
                shading = 'flat'

        C = cbook.safe_masked_invalid(C)
        return X, Y, C, shading
