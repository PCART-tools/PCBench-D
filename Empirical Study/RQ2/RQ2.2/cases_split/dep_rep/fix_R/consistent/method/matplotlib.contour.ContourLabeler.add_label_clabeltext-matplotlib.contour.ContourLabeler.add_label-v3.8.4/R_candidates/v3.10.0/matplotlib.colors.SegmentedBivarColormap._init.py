    def _init(self):
        s = self.patch.shape
        _patch = np.empty((s[0], s[1], 4))
        _patch[:, :, :3] = self.patch
        _patch[:, :, 3] = 1
        transform = mpl.transforms.Affine2D().translate(-0.5, -0.5)\
                                .scale(self.N / (s[1] - 1), self.N / (s[0] - 1))
        self._lut = np.empty((self.N, self.N, 4))

        _image.resample(_patch, self._lut, transform, _image.BILINEAR,
                        resample=False, alpha=1)
        self._isinit = True
