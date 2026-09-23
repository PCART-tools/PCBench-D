    @property
    def angles(self):
        """The internal angle at each vertex.

        Returns
        =======

        angles : dict
            A dictionary where each key is a vertex and each value is the
            internal angle at that vertex. The vertices are represented as
            Points.

        See Also
        ========

        sympy.geometry.point.Point, sympy.geometry.line.LinearEntity.angle_between

        Examples
        ========

        >>> from sympy import Point, Polygon
        >>> p1, p2, p3, p4 = map(Point, [(0, 0), (1, 0), (5, 1), (0, 1)])
        >>> poly = Polygon(p1, p2, p3, p4)
        >>> poly.angles[p1]
        pi/2
        >>> poly.angles[p2]
        acos(-4*sqrt(17)/17)

        """

        # Determine orientation of points
        args = self.vertices
        cw = self._isright(args[-1], args[0], args[1])

        ret = {}
        for i in range(len(args)):
            a, b, c = args[i - 2], args[i - 1], args[i]
            ang = Ray(b, a).angle_between(Ray(b, c))
            if cw ^ self._isright(a, b, c):
                ret[b] = 2*S.Pi - ang
            else:
                ret[b] = ang
        return ret
