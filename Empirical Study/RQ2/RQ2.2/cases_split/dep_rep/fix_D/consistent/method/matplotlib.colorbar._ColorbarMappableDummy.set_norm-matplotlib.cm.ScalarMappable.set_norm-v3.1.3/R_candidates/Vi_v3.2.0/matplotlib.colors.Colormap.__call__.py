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
        Tuple of RGBA values if X is scalar, otherwise an array of
        RGBA values with a shape of ``X.shape + (4, )``.

        """
        # See class docstring for arg/kwarg documentation.
        if not self._isinit:
            self._init()
        mask_bad = None
        if np.ma.is_masked(X):
            mask_bad = X.mask
        elif np.any(np.isnan(X)):
            # mask nan's
            mask_bad = np.isnan(X)

        xa = np.array(X, copy=True)
        # Fill bad values to avoid warnings
        # in the boolean comparisons below.
        if mask_bad is not None:
            xa[mask_bad] = 0.

        # Calculations with native byteorder are faster, and avoid a
        # bug that otherwise can occur with putmask when the last
        # argument is a numpy scalar.
        if not xa.dtype.isnative:
            xa = xa.byteswap().newbyteorder()

        if xa.dtype.kind == "f":
            xa *= self.N
            # Negative values are out of range, but astype(int) would truncate
            # them towards zero.
            xa[xa < 0] = -1
            # xa == 1 (== N after multiplication) is not out of range.
            xa[xa == self.N] = self.N - 1
            # Avoid converting large positive values to negative integers.
            np.clip(xa, -1, self.N, out=xa)
            xa = xa.astype(int)
        # Set the over-range indices before the under-range;
        # otherwise the under-range values get converted to over-range.
        xa[xa > self.N - 1] = self._i_over
        xa[xa < 0] = self._i_under
        if mask_bad is not None:
            xa[mask_bad] = self._i_bad

        if bytes:
            lut = (self._lut * 255).astype(np.uint8)
        else:
            lut = self._lut.copy()  # Don't let alpha modify original _lut.

        if alpha is not None:
            alpha = np.clip(alpha, 0, 1)
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

        rgba = lut.take(xa, axis=0, mode='clip')
        if not np.iterable(X):
            # Return a tuple if the input was a scalar
            rgba = tuple(rgba)
        return rgba
