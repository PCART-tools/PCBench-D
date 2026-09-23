    def __str__(self):
        s = "RegularPolygon((%g, %g), %d, radius=%g, orientation=%g)"
        return s % (self._xy[0], self._xy[1], self._numVertices, self._radius,
                    self._orientation)
