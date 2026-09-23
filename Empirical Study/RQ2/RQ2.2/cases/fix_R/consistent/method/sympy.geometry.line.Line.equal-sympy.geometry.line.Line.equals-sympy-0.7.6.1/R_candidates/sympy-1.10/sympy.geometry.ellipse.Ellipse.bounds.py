    @property
    def bounds(self):
        """Return a tuple (xmin, ymin, xmax, ymax) representing the bounding
        rectangle for the geometric figure.

        """

        h, v = self.hradius, self.vradius
        return (self.center.x - h, self.center.y - v, self.center.x + h, self.center.y + v)
