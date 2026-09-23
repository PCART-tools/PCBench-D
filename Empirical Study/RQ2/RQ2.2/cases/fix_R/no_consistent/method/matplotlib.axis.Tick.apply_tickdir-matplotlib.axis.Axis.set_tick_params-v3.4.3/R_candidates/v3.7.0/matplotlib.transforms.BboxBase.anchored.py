    def anchored(self, c, container=None):
        """
        Return a copy of the `Bbox` anchored to *c* within *container*.

        Parameters
        ----------
        c : (float, float) or {'C', 'SW', 'S', 'SE', 'E', 'NE', ...}
            Either an (*x*, *y*) pair of relative coordinates (0 is left or
            bottom, 1 is right or top), 'C' (center), or a cardinal direction
            ('SW', southwest, is bottom left, etc.).
        container : `Bbox`, optional
            The box within which the `Bbox` is positioned; it defaults
            to the initial `Bbox`.

        See Also
        --------
        .Axes.set_anchor
        """
        if container is None:
            container = self
        l, b, w, h = container.bounds
        if isinstance(c, str):
            cx, cy = self.coefs[c]
        else:
            cx, cy = c
        L, B, W, H = self.bounds
        return Bbox(self._points +
                    [(l + cx * (w - W)) - L,
                     (b + cy * (h - H)) - B])
