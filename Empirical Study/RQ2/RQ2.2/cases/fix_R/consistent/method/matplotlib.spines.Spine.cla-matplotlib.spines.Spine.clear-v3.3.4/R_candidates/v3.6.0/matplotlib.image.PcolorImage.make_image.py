    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        if self._A is None:
            raise RuntimeError('You must first set the image array')
        if unsampled:
            raise ValueError('unsampled not supported on PColorImage')

        if self._imcache is None:
            A = self.to_rgba(self._A, bytes=True)
            self._imcache = np.pad(A, [(1, 1), (1, 1), (0, 0)], "constant")
        padded_A = self._imcache
        bg = mcolors.to_rgba(self.axes.patch.get_facecolor(), 0)
        bg = (np.array(bg) * 255).astype(np.uint8)
        if (padded_A[0, 0] != bg).all():
            padded_A[[0, -1], :] = padded_A[:, [0, -1]] = bg

        l, b, r, t = self.axes.bbox.extents
        width = (round(r) + 0.5) - (round(l) - 0.5)
        height = (round(t) + 0.5) - (round(b) - 0.5)
        width = int(round(width * magnification))
        height = int(round(height * magnification))
        vl = self.axes.viewLim

        x_pix = np.linspace(vl.x0, vl.x1, width)
        y_pix = np.linspace(vl.y0, vl.y1, height)
        x_int = self._Ax.searchsorted(x_pix)
        y_int = self._Ay.searchsorted(y_pix)
        im = (  # See comment in NonUniformImage.make_image re: performance.
            padded_A.view(np.uint32).ravel()[
                np.add.outer(y_int * padded_A.shape[1], x_int)]
            .view(np.uint8).reshape((height, width, 4)))
        return im, l, b, IdentityTransform()
