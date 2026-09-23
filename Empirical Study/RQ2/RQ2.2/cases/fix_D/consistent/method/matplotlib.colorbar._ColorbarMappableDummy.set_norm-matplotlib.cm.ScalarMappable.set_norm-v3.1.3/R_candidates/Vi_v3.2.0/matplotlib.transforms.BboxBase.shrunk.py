    def shrunk(self, mx, my):
        """
        Return a copy of the :class:`Bbox`, shrunk by the factor *mx*
        in the *x* direction and the factor *my* in the *y* direction.
        The lower left corner of the box remains unchanged.  Normally
        *mx* and *my* will be less than 1, but this is not enforced.
        """
        w, h = self.size
        return Bbox([self._points[0],
                    self._points[0] + [mx * w, my * h]])
