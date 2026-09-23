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
        # The extra cast-to-int is only needed for python2
        width = int(round(width * magnification))
        height = int(round(height * magnification))
        if self._rgbacache is None:
            A = self.to_rgba(self._A, bytes=True)
            self._rgbacache = A
            if self._A.ndim == 2:
                self.is_grayscale = self.cmap.is_gray()
        else:
            A = self._rgbacache
        vl = self.axes.viewLim
        im = _image.pcolor2(self._Ax, self._Ay, A,
                            height,
                            width,
                            (vl.x0, vl.x1, vl.y0, vl.y1),
                            bg)
        return im, l, b, IdentityTransform()
