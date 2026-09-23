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
                self.is_grayscale = self.cmap.is_gray()
            else:
                A = np.repeat(A[:, :, np.newaxis], 4, 2)
                A[:, :, 3] = 255
                self.is_grayscale = True
        else:
            if A.dtype != np.uint8:
                A = (255*A).astype(np.uint8)
            if A.shape[2] == 3:
                B = np.zeros(tuple([*A.shape[0:2], 4]), np.uint8)
                B[:, :, 0:3] = A
                B[:, :, 3] = 255
                A = B
            self.is_grayscale = False
        x0, y0, v_width, v_height = self.axes.viewLim.bounds
        l, b, r, t = self.axes.bbox.extents
        width = (np.round(r) + 0.5) - (np.round(l) - 0.5)
        height = (np.round(t) + 0.5) - (np.round(b) - 0.5)
        width *= magnification
        height *= magnification
        im = _image.pcolor(self._Ax, self._Ay, A,
                           int(height), int(width),
                           (x0, x0+v_width, y0, y0+v_height),
                           _interpd_[self._interpolation])
        return im, l, b, IdentityTransform()
