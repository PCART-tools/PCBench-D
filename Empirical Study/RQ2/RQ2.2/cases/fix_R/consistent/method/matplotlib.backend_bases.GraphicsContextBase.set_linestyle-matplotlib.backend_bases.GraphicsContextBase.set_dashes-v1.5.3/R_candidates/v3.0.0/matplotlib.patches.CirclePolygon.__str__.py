    def __str__(self):
        s = "CirclePolygon((%g, %g), radius=%g, resolution=%d)"
        return s % (self._xy[0], self._xy[1], self._radius, self._numVertices)
