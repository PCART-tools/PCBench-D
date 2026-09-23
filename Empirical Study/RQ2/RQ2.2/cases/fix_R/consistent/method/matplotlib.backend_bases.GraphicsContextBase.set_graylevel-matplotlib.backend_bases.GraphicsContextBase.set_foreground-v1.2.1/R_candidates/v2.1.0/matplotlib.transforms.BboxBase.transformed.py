    def transformed(self, transform):
        """
        Return a new :class:`Bbox` object, statically transformed by
        the given transform.
        """
        pts = self.get_points()
        ll, ul, lr = transform.transform(np.array([pts[0],
            [pts[0, 0], pts[1, 1]], [pts[1, 0], pts[0, 1]]]))
        return Bbox([ll, [lr[0], ul[1]]])
