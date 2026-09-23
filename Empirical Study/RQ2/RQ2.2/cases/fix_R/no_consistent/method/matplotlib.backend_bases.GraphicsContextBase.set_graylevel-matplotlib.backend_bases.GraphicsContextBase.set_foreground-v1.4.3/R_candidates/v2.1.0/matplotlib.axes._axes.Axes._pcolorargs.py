    @staticmethod
    def _pcolorargs(funcname, *args, **kw):
        # This takes one kwarg, allmatch.
        # If allmatch is True, then the incoming X, Y, C must
        # have matching dimensions, taking into account that
        # X and Y can be 1-D rather than 2-D.  This perfect
        # match is required for Gouroud shading.  For flat
        # shading, X and Y specify boundaries, so we need
        # one more boundary than color in each direction.
        # For convenience, and consistent with Matlab, we
        # discard the last row and/or column of C if necessary
        # to meet this condition.  This is done if allmatch
        # is False.

        allmatch = kw.pop("allmatch", False)

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
            X, Y, C = [np.asanyarray(a) for a in args]
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
            if not (Nx == numCols and Ny == numRows):
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
