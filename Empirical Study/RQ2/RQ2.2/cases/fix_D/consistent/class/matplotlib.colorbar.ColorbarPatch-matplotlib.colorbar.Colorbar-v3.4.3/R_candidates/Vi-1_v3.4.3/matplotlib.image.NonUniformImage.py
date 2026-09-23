class NonUniformImage(AxesImage):
    mouseover = False  # This class still needs its own get_cursor_data impl.

    def __init__(self, ax, *, interpolation='nearest', **kwargs):
        """
        Parameters
        ----------
        interpolation : {'nearest', 'bilinear'}, default: 'nearest'

        **kwargs
            All other keyword arguments are identical to those of `.AxesImage`.
        """
        super().__init__(ax, **kwargs)
        self.set_interpolation(interpolation)

    def _check_unsampled_image(self):
        """Return False. Do not use unsampled image."""
        return False

    is_grayscale = _api.deprecate_privatize_attribute("3.3")

    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        if self._A is None:
            raise RuntimeError('You must first set the image array')
        if unsampled:
            raise ValueError('unsampled not supported on NonUniformImage')
        A = self._A
        if A.ndim == 2:
            if A.dtype != np.uint8:
                A = self.to_rgba(A, bytes=True)
                self._is_grayscale = self.cmap.is_gray()
            else:
                A = np.repeat(A[:, :, np.newaxis], 4, 2)
                A[:, :, 3] = 255
                self._is_grayscale = True
        else:
            if A.dtype != np.uint8:
                A = (255*A).astype(np.uint8)
            if A.shape[2] == 3:
                B = np.zeros(tuple([*A.shape[0:2], 4]), np.uint8)
                B[:, :, 0:3] = A
                B[:, :, 3] = 255
                A = B
            self._is_grayscale = False
        vl = self.axes.viewLim
        l, b, r, t = self.axes.bbox.extents
        width = (round(r) + 0.5) - (round(l) - 0.5)
        height = (round(t) + 0.5) - (round(b) - 0.5)
        width *= magnification
        height *= magnification
        im = _image.pcolor(self._Ax, self._Ay, A,
                           int(height), int(width),
                           (vl.x0, vl.x1, vl.y0, vl.y1),
                           _interpd_[self._interpolation])
        return im, l, b, IdentityTransform()

    def set_data(self, x, y, A):
        """
        Set the grid for the pixel centers, and the pixel values.

        Parameters
        ----------
        x, y : 1D array-like
            Monotonic arrays of shapes (N,) and (M,), respectively, specifying
            pixel centers.
        A : array-like
            (M, N) ndarray or masked array of values to be colormapped, or
            (M, N, 3) RGB array, or (M, N, 4) RGBA array.
        """
        x = np.array(x, np.float32)
        y = np.array(y, np.float32)
        A = cbook.safe_masked_invalid(A, copy=True)
        if not (x.ndim == y.ndim == 1 and A.shape[0:2] == y.shape + x.shape):
            raise TypeError("Axes don't match array shape")
        if A.ndim not in [2, 3]:
            raise TypeError("Can only plot 2D or 3D data")
        if A.ndim == 3 and A.shape[2] not in [1, 3, 4]:
            raise TypeError("3D arrays must have three (RGB) "
                            "or four (RGBA) color components")
        if A.ndim == 3 and A.shape[2] == 1:
            A = A.squeeze(axis=-1)
        self._A = A
        self._Ax = x
        self._Ay = y
        self._imcache = None

        self.stale = True

    def set_array(self, *args):
        raise NotImplementedError('Method not supported')

    def set_interpolation(self, s):
        """
        Parameters
        ----------
        s : {'nearest', 'bilinear'} or None
            If None, use :rc:`image.interpolation`.
        """
        if s is not None and s not in ('nearest', 'bilinear'):
            raise NotImplementedError('Only nearest neighbor and '
                                      'bilinear interpolations are supported')
        super().set_interpolation(s)

    def get_extent(self):
        if self._A is None:
            raise RuntimeError('Must set data first')
        return self._Ax[0], self._Ax[-1], self._Ay[0], self._Ay[-1]

    def set_filternorm(self, s):
        pass

    def set_filterrad(self, s):
        pass

    def set_norm(self, norm):
        if self._A is not None:
            raise RuntimeError('Cannot change colors after loading data')
        super().set_norm(norm)

    def set_cmap(self, cmap):
        if self._A is not None:
            raise RuntimeError('Cannot change colors after loading data')
        super().set_cmap(cmap)
