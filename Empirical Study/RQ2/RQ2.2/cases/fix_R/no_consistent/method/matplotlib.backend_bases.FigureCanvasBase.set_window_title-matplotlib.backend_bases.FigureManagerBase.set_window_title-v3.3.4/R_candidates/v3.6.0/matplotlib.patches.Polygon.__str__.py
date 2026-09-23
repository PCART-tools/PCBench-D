    def __str__(self):
        if len(self._path.vertices):
            s = "Polygon%d((%g, %g) ...)"
            return s % (len(self._path.vertices), *self._path.vertices[0])
        else:
            return "Polygon0()"
