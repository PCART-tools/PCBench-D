    def __call__(self, renderer):
        """
        Return the offset transform.

        Parameters
        ----------
        renderer : `RendererBase`
            The renderer to use to compute the offset

        Returns
        -------
        `Transform`
            Maps (x, y) in pixel or point units to screen units
            relative to the given artist.
        """
        if isinstance(self._artist, Artist):
            bbox = self._artist.get_window_extent(renderer)
            xf, yf = self._ref_coord
            x = bbox.x0 + bbox.width * xf
            y = bbox.y0 + bbox.height * yf
        elif isinstance(self._artist, BboxBase):
            bbox = self._artist
            xf, yf = self._ref_coord
            x = bbox.x0 + bbox.width * xf
            y = bbox.y0 + bbox.height * yf
        elif isinstance(self._artist, Transform):
            x, y = self._artist.transform(self._ref_coord)
        else:
            raise RuntimeError("unknown type")

        sc = self._get_scale(renderer)
        tr = Affine2D().scale(sc).translate(x, y)

        return tr
