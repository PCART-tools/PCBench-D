    @classmethod
    def unit_regular_polygon(cls, numVertices):
        """
        Return a :class:`Path` instance for a unit regular polygon with the
        given *numVertices* and radius of 1.0, centered at (0, 0).
        """
        if numVertices <= 16:
            path = cls._unit_regular_polygons.get(numVertices)
        else:
            path = None
        if path is None:
            theta = ((2 * np.pi / numVertices) * np.arange(numVertices + 1)
                     # This initial rotation is to make sure the polygon always
                     # "points-up".
                     + np.pi / 2)
            verts = np.column_stack((np.cos(theta), np.sin(theta)))
            codes = np.empty(numVertices + 1)
            codes[0] = cls.MOVETO
            codes[1:-1] = cls.LINETO
            codes[-1] = cls.CLOSEPOLY
            path = cls(verts, codes, readonly=True)
            if numVertices <= 16:
                cls._unit_regular_polygons[numVertices] = path
        return path
