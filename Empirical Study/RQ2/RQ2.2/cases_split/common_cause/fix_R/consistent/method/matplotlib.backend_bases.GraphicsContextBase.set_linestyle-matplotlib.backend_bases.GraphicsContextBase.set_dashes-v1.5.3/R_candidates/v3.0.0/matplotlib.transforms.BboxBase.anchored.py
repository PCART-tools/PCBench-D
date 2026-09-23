    def anchored(self, c, container=None):
        """
        Return a copy of the :class:`Bbox`, shifted to position *c*
        within a container.

        Parameters
        ----------
        c :
            May be either:

            * A sequence (*cx*, *cy*) where *cx* and *cy* range from 0
              to 1, where 0 is left or bottom and 1 is right or top

            * a string:
              - 'C' for centered
              - 'S' for bottom-center
              - 'SE' for bottom-left
              - 'E' for left
              - etc.

        container : Bbox, optional
            The box within which the :class:`Bbox` is positioned; it defaults
            to the initial :class:`Bbox`.
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
