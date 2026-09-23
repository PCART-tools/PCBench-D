    def corners(self):
        """
        Return an array of points which are the four corners of this
        rectangle.  For example, if this :class:`Bbox` is defined by
        the points (*a*, *b*) and (*c*, *d*), :meth:`corners` returns
        (*a*, *b*), (*a*, *d*), (*c*, *b*) and (*c*, *d*).
        """
        l, b, r, t = self.get_points().flatten()
        return np.array([[l, b], [l, t], [r, b], [r, t]])
