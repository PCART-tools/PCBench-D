    def _pcolorargs(self, funcname, *args, shading='auto', **kwargs):
        # - create X and Y if not present;
        # - reshape X and Y as needed if they are 1-D;
        # - check for proper sizes based on `shading` kwarg;
        # - reset shading if shading='auto' to flat or nearest
        #   depending on size;

        _valid_shading = ['gouraud', 'nearest', 'flat', 'auto']
        try:
            _api.check_in_list(_valid_shading, shading=shading)
        except ValueError:
            _api.warn_external(f"shading value '{shading}' not in list of "
                               f"valid values {_valid_shading}. Setting "
                               "shading='auto'.")
            shading = 'auto'

        if len(args) == 1:
            C = np.asanyarray(args[0])
            nrows, ncols = C.shape[:2]
            if shading in ['gouraud', 'nearest']:
                X, Y = np.meshgrid(np.arange(ncols), np.arange(nrows))
            else:
                X, Y = np.meshgrid(np.arange(ncols + 1), np.arange(nrows + 1))
                shading = 'flat'
        elif len(args) == 3:
            # Check x and y for bad data...
            C = np.asanyarray(args[2])
            # unit conversion allows e.g. datetime objects as axis values
            X, Y = args[:2]
            X, Y = self._process_unit_info([("x", X), ("y", Y)], kwargs)
            X, Y = (cbook.safe_masked_invalid(a, copy=True) for a in [X, Y])

            if funcname == 'pcolormesh':
                if np.ma.is_masked(X) or np.ma.is_masked(Y):
                    raise ValueError(
                        'x and y arguments to pcolormesh cannot have '
                        'non-finite values or be of type '
                        'numpy.ma.MaskedArray with masked values')
            nrows, ncols = C.shape[:2]
        else:
            raise _api.nargs_error(funcname, takes="1 or 3", given=len(args))

        Nx = X.shape[-1]
        Ny = Y.shape[0]
        if X.ndim != 2 or X.shape[0] == 1:
            x = X.reshape(1, Nx)
            X = x.repeat(Ny, axis=0)
        if Y.ndim != 2 or Y.shape[1] == 1:
            y = Y.reshape(Ny, 1)
            Y = y.repeat(Nx, axis=1)
        if X.shape != Y.shape:
            raise TypeError(f'Incompatible X, Y inputs to {funcname}; '
                            f'see help({funcname})')

        if shading == 'auto':
            if ncols == Nx and nrows == Ny:
                shading = 'nearest'
            else:
                shading = 'flat'

        if shading == 'flat':
            if (Nx, Ny) != (ncols + 1, nrows + 1):
                raise TypeError(f"Dimensions of C {C.shape} should"
                                f" be one smaller than X({Nx}) and Y({Ny})"
                                f" while using shading='flat'"
                                f" see help({funcname})")
        else:    # ['nearest', 'gouraud']:
            if (Nx, Ny) != (ncols, nrows):
                raise TypeError('Dimensions of C %s are incompatible with'
                                ' X (%d) and/or Y (%d); see help(%s)' % (
                                    C.shape, Nx, Ny, funcname))
            if shading == 'nearest':
                # grid is specified at the center, so define corners
                # at the midpoints between the grid centers and then use the
                # flat algorithm.
                def _interp_grid(X, require_monotonicity=False):
                    # helper for below. To ensure the cell edges are calculated
                    # correctly, when expanding columns, the monotonicity of
                    # X coords needs to be checked. When expanding rows, the
                    # monotonicity of Y coords needs to be checked.
                    if np.shape(X)[1] > 1:
                        dX = np.diff(X, axis=1) * 0.5
                        if (require_monotonicity and
                                not (np.all(dX >= 0) or np.all(dX <= 0))):
                            _api.warn_external(
                                f"The input coordinates to {funcname} are "
                                "interpreted as cell centers, but are not "
                                "monotonically increasing or decreasing. "
                                "This may lead to incorrectly calculated cell "
                                "edges, in which case, please supply "
                                f"explicit cell edges to {funcname}.")

                        hstack = np.ma.hstack if np.ma.isMA(X) else np.hstack
                        X = hstack((X[:, [0]] - dX[:, [0]],
                                    X[:, :-1] + dX,
                                    X[:, [-1]] + dX[:, [-1]]))
                    else:
                        # This is just degenerate, but we can't reliably guess
                        # a dX if there is just one value.
                        X = np.hstack((X, X))
                    return X

                if ncols == Nx:
                    X = _interp_grid(X, require_monotonicity=True)
                    Y = _interp_grid(Y)
                if nrows == Ny:
                    X = _interp_grid(X.T).T
                    Y = _interp_grid(Y.T, require_monotonicity=True).T
                shading = 'flat'

        C = cbook.safe_masked_invalid(C, copy=True)
        return X, Y, C, shading
