class PcolorImage(AxesImage):
    """
    Make a pcolor-style plot with an irregular rectangular grid.

    This uses a variation of the original irregular image code,
    and it is used by pcolorfast for the corresponding grid type.
    """
    def __init__(self, ax,
                 x=None,
                 y=None,
                 A=None,
                 cmap=None,
                 norm=None,
                 **kwargs
                 ):
        """
        Parameters
        ----------
        ax : `~.axes.Axes`
            The axes the image will belong to.
        x, y : 1D array-like, optional
            Monotonic arrays of length N+1 and M+1, respectively, specifying
            rectangle boundaries.  If not given, will default to
            ``range(N + 1)`` and ``range(M + 1)``, respectively.
        A : array-like
            The data to be color-coded. The interpretation depends on the
            shape:

            - (M, N) ndarray or masked array: values to be colormapped
            - (M, N, 3): RGB array
            - (M, N, 4): RGBA array

        cmap : str or `~matplotlib.colors.Colormap`, default: :rc:`image.cmap`
            The Colormap instance or registered colormap name used to map
            scalar data to colors.
        norm : `~matplotlib.colors.Normalize`
            Maps luminance to 0-1.
        **kwargs : `.Artist` properties
        """
        super().__init__(ax, norm=norm, cmap=cmap)
        self.update(kwargs)
        if A is not None:
            self.set_data(x, y, A)

    is_grayscale = _api.deprecate_privatize_attribute("3.3")

    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        if self._A is None:
            raise RuntimeError('You must first set the image array')
        if unsampled:
            raise ValueError('unsampled not supported on PColorImage')
        fc = self.axes.patch.get_facecolor()
        bg = mcolors.to_rgba(fc, 0)
        bg = (np.array(bg)*255).astype(np.uint8)
        l, b, r, t = self.axes.bbox.extents
        width = (round(r) + 0.5) - (round(l) - 0.5)
        height = (round(t) + 0.5) - (round(b) - 0.5)
        width = int(round(width * magnification))
        height = int(round(height * magnification))
        if self._rgbacache is None:
            A = self.to_rgba(self._A, bytes=True)
            self._rgbacache = A
            if self._A.ndim == 2:
                self._is_grayscale = self.cmap.is_gray()
        else:
            A = self._rgbacache
        vl = self.axes.viewLim
        im = _image.pcolor2(self._Ax, self._Ay, A,
                            height,
                            width,
                            (vl.x0, vl.x1, vl.y0, vl.y1),
                            bg)
        return im, l, b, IdentityTransform()

    def _check_unsampled_image(self):
        return False

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

            - (M, N) ndarray or masked array: values to be colormapped
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
        if A.ndim == 3 and A.shape[2] == 1:
            A = A.squeeze(axis=-1)
        self._is_grayscale = False
        if A.ndim == 3:
            if A.shape[2] in [3, 4]:
                if ((A[:, :, 0] == A[:, :, 1]).all() and
                        (A[:, :, 0] == A[:, :, 2]).all()):
                    self._is_grayscale = True
            else:
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
        self._rgbacache = None
        self.stale = True

    def set_array(self, *args):
        raise NotImplementedError('Method not supported')

    def get_cursor_data(self, event):
        # docstring inherited
        x, y = event.xdata, event.ydata
        if (x < self._Ax[0] or x > self._Ax[-1] or
                y < self._Ay[0] or y > self._Ay[-1]):
            return None
        j = np.searchsorted(self._Ax, x) - 1
        i = np.searchsorted(self._Ay, y) - 1
        try:
            return self._A[i, j]
        except IndexError:
            return None
