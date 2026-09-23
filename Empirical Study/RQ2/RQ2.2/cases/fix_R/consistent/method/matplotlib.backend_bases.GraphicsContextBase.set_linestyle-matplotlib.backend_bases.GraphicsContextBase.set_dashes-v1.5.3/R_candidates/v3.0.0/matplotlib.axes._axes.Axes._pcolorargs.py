    @staticmethod
    def _pcolorargs(funcname, *args, allmatch=False):
        # If allmatch is True, then the incoming X, Y, C must have matching
        # dimensions, taking into account that X and Y can be 1-D rather than
        # 2-D.  This perfect match is required for Gouroud shading.  For flat
        # shading, X and Y specify boundaries, so we need one more boundary
        # than color in each direction.  For convenience, and consistent with
        # Matlab, we discard the last row and/or column of C if necessary to
        # meet this condition.  This is done if allmatch is False.

        if len(args) == 1:
            C = np.asanyarray(args[0])
            numRows, numCols = C.shape
            if allmatch:
                X, Y = np.meshgrid(np.arange(numCols), np.arange(numRows))
            else:
                X, Y = np.meshgrid(np.arange(numCols + 1),
                                   np.arange(numRows + 1))
            C = cbook.safe_masked_invalid(C)
            return X, Y, C

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
            numRows, numCols = C.shape
        else:
            raise TypeError(
                'Illegal arguments to %s; see help(%s)' % (funcname, funcname))

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
        if allmatch:
            if (Nx, Ny) != (numCols, numRows):
                raise TypeError('Dimensions of C %s are incompatible with'
                                ' X (%d) and/or Y (%d); see help(%s)' % (
                                    C.shape, Nx, Ny, funcname))
        else:
            if not (numCols in (Nx, Nx - 1) and numRows in (Ny, Ny - 1)):
                raise TypeError('Dimensions of C %s are incompatible with'
                                ' X (%d) and/or Y (%d); see help(%s)' % (
                                    C.shape, Nx, Ny, funcname))
            C = C[:Ny - 1, :Nx - 1]
        C = cbook.safe_masked_invalid(C)
        return X, Y, C
