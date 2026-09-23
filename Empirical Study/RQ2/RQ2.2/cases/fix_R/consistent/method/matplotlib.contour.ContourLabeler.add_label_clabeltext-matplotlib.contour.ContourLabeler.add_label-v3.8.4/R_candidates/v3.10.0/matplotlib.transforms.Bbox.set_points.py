    def set_points(self, points):
        """
        Set the points of the bounding box directly from an array of the form
        ``[[x0, y0], [x1, y1]]``.  No error checking is performed, as this
        method is mainly for internal use.
        """
        if np.any(self._points != points):
            self._points = points
            self.invalidate()
