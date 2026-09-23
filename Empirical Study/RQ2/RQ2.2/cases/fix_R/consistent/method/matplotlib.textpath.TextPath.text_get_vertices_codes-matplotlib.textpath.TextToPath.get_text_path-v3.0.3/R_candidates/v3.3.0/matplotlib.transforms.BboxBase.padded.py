    def padded(self, p):
        """Construct a `Bbox` by padding this one on all four sides by *p*."""
        points = self.get_points()
        return Bbox(points + [[-p, -p], [p, p]])
