    def padded(self, p):
        """
        Return a new :class:`Bbox` that is padded on all four sides by
        the given value.
        """
        points = self.get_points()
        return Bbox(points + [[-p, -p], [p, p]])
