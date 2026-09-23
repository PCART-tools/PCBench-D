    def corners(self):
        """
        Return the corners of this rectangle as an array of points.

        Specifically, this returns the array
        ``[[x0, y0], [x0, y1], [x1, y0], [x1, y1]]``.
        """
        (x0, y0), (x1, y1) = self.get_points()
        return np.array([[x0, y0], [x0, y1], [x1, y0], [x1, y1]])
