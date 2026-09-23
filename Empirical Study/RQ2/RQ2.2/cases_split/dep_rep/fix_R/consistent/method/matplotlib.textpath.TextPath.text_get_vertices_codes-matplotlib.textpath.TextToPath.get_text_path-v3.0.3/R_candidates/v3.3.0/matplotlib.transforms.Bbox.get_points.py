    def get_points(self):
        """
        Get the points of the bounding box directly as a numpy array
        of the form: ``[[x0, y0], [x1, y1]]``.
        """
        self._invalid = 0
        return self._points
