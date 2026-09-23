    def __call__(self, renderer):
        '''
        Return the offset transform.

        Parameters
        ----------
        renderer : `RendererBase`
            The renderer to use to compute the offset

        Returns
        -------
        transform : `Transform`
            Maps (x, y) in pixel or point units to screen units
            relative to the given artist.
        '''
        if isinstance(self._artist, Artist):
            bbox = self._artist.get_window_extent(renderer)
            l, b, w, h = bbox.bounds
            xf, yf = self._ref_coord
            x, y = l + w * xf, b + h * yf
        elif isinstance(self._artist, BboxBase):
            l, b, w, h = self._artist.bounds
            xf, yf = self._ref_coord
            x, y = l + w * xf, b + h * yf
        elif isinstance(self._artist, Transform):
            x, y = self._artist.transform(self._ref_coord)
        else:
            raise RuntimeError("unknown type")

        sc = self._get_scale(renderer)
        tr = Affine2D().scale(sc).translate(x, y)

        return tr
