    def __call__(self, X, alpha=None, bytes=False):
        r"""
        Parameters
        ----------
        X : tuple (X0, X1), X0 and X1: float or int `~numpy.ndarray` or scalar
            The data value(s) to convert to RGBA.

            - For floats, *X* should be in the interval ``[0.0, 1.0]`` to
              return the RGBA values ``X*100`` percent along the Colormap.
            - For integers, *X* should be in the interval ``[0, Colormap.N)`` to
              return RGBA values *indexed* from the Colormap with index ``X``.

        alpha : float or array-like or None, default: None
            Alpha must be a scalar between 0 and 1, a sequence of such
            floats with shape matching X0, or None.
        bytes : bool, default: False
            If False (default), the returned RGBA values will be floats in the
            interval ``[0, 1]`` otherwise they will be `numpy.uint8`\s in the
            interval ``[0, 255]``.

        Returns
        -------
        Tuple of RGBA values if X is scalar, otherwise an array of
        RGBA values with a shape of ``X.shape + (4, )``.
        """

        if len(X) != 2:
            raise ValueError(
                f'For a `BivarColormap` the data must have a first dimension '
                f'2, not {len(X)}')

        if not self._isinit:
            self._init()

        X0 = np.ma.array(X[0], copy=True)
        X1 = np.ma.array(X[1], copy=True)
        # clip to shape of colormap, circle square, etc.
        self._clip((X0, X1))

        # Native byteorder is faster.
        if not X0.dtype.isnative:
            X0 = X0.byteswap().view(X0.dtype.newbyteorder())
        if not X1.dtype.isnative:
            X1 = X1.byteswap().view(X1.dtype.newbyteorder())

        if X0.dtype.kind == "f":
            X0 *= self.N
            # xa == 1 (== N after multiplication) is not out of range.
            X0[X0 == self.N] = self.N - 1

        if X1.dtype.kind == "f":
            X1 *= self.M
            # xa == 1 (== N after multiplication) is not out of range.
            X1[X1 == self.M] = self.M - 1

        # Pre-compute the masks before casting to int (which can truncate)
        mask_outside = (X0 < 0) | (X1 < 0) | (X0 >= self.N) | (X1 >= self.M)
        # If input was masked, get the bad mask from it; else mask out nans.
        mask_bad_0 = X0.mask if np.ma.is_masked(X0) else np.isnan(X0)
        mask_bad_1 = X1.mask if np.ma.is_masked(X1) else np.isnan(X1)
        mask_bad = mask_bad_0 | mask_bad_1

        with np.errstate(invalid="ignore"):
            # We need this cast for unsigned ints as well as floats
            X0 = X0.astype(int)
            X1 = X1.astype(int)

        # Set masked values to zero
        # The corresponding rgb values will be replaced later
        for X_part in [X0, X1]:
            X_part[mask_outside] = 0
            X_part[mask_bad] = 0

        rgba = self._lut[X0, X1]
        if np.isscalar(X[0]):
            rgba = np.copy(rgba)
        rgba[mask_outside] = self._rgba_outside
        rgba[mask_bad] = self._rgba_bad
        if bytes:
            rgba = (rgba * 255).astype(np.uint8)
        if alpha is not None:
            alpha = np.clip(alpha, 0, 1)
            if bytes:
                alpha *= 255  # Will be cast to uint8 upon assignment.
            if np.shape(alpha) not in [(), np.shape(X0)]:
                raise ValueError(
                    f"alpha is array-like but its shape {np.shape(alpha)} does "
                    f"not match that of X[0] {np.shape(X0)}")
            rgba[..., -1] = alpha
            # If the "bad" color is all zeros, then ignore alpha input.
            if (np.array(self._rgba_bad) == 0).all():
                rgba[mask_bad] = (0, 0, 0, 0)

        if not np.iterable(X[0]):
            rgba = tuple(rgba)
        return rgba
