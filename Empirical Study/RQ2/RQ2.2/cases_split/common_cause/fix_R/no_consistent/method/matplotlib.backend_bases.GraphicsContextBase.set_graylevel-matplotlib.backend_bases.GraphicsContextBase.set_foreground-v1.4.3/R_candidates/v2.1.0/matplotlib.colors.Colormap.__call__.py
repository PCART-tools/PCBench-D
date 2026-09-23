    def __call__(self, X, alpha=None, bytes=False):
        """
        Parameters
        ----------
        X : scalar, ndarray
            The data value(s) to convert to RGBA.
            For floats, X should be in the interval ``[0.0, 1.0]`` to
            return the RGBA values ``X*100`` percent along the Colormap line.
            For integers, X should be in the interval ``[0, Colormap.N)`` to
            return RGBA values *indexed* from the Colormap with index ``X``.
        alpha : float, None
            Alpha must be a scalar between 0 and 1, or None.
        bytes : bool
            If False (default), the returned RGBA values will be floats in the
            interval ``[0, 1]`` otherwise they will be uint8s in the interval
            ``[0, 255]``.

        Returns
        -------
        Tuple of RGBA values if X is scalar, othewise an array of
        RGBA values with a shape of ``X.shape + (4, )``.

        """
        # See class docstring for arg/kwarg documentation.
        if not self._isinit:
            self._init()
        mask_bad = None
        if not cbook.iterable(X):
            vtype = 'scalar'
            xa = np.array([X])
        else:
            vtype = 'array'
            xma = np.ma.array(X, copy=True)  # Copy here to avoid side effects.
            mask_bad = xma.mask              # Mask will be used below.
            xa = xma.filled()                # Fill to avoid infs, etc.
            del xma

        # Calculations with native byteorder are faster, and avoid a
        # bug that otherwise can occur with putmask when the last
        # argument is a numpy scalar.
        if not xa.dtype.isnative:
            xa = xa.byteswap().newbyteorder()

        if xa.dtype.kind == "f":
            # Treat 1.0 as slightly less than 1.
            vals = np.array([1, 0], dtype=xa.dtype)
            almost_one = np.nextafter(*vals)
            np.copyto(xa, almost_one, where=xa == 1.0)
            # The following clip is fast, and prevents possible
            # conversion of large positive values to negative integers.

            xa *= self.N
            np.clip(xa, -1, self.N, out=xa)

            # ensure that all 'under' values will still have negative
            # value after casting to int
            np.copyto(xa, -1, where=xa < 0.0)
            xa = xa.astype(int)
        # Set the over-range indices before the under-range;
        # otherwise the under-range values get converted to over-range.
        np.copyto(xa, self._i_over, where=xa > self.N - 1)
        np.copyto(xa, self._i_under, where=xa < 0)
        if mask_bad is not None:
            if mask_bad.shape == xa.shape:
                np.copyto(xa, self._i_bad, where=mask_bad)
            elif mask_bad:
                xa.fill(self._i_bad)
        if bytes:
            lut = (self._lut * 255).astype(np.uint8)
        else:
            lut = self._lut.copy()  # Don't let alpha modify original _lut.

        if alpha is not None:
            alpha = min(alpha, 1.0)  # alpha must be between 0 and 1
            alpha = max(alpha, 0.0)
            if bytes:
                alpha = int(alpha * 255)
            if (lut[-1] == 0).all():
                lut[:-1, -1] = alpha
                # All zeros is taken as a flag for the default bad
                # color, which is no color--fully transparent.  We
                # don't want to override this.
            else:
                lut[:, -1] = alpha
                # If the bad value is set to have a color, then we
                # override its alpha just as for any other value.

        rgba = np.empty(shape=xa.shape + (4,), dtype=lut.dtype)
        lut.take(xa, axis=0, mode='clip', out=rgba)
        if vtype == 'scalar':
            rgba = tuple(rgba[0, :])
        return rgba
