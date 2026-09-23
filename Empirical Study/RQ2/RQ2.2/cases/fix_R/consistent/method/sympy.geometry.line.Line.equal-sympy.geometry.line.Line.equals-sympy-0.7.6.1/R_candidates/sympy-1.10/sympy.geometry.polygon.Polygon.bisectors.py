    def bisectors(p, prec=None):
        """Returns angle bisectors of a polygon. If prec is given
        then approximate the point defining the ray to that precision.

        The distance between the points defining the bisector ray is 1.

        Examples
        ========

        >>> from sympy import Polygon, Point
        >>> p = Polygon(Point(0, 0), Point(2, 0), Point(1, 1), Point(0, 3))
        >>> p.bisectors(2)
        {Point2D(0, 0): Ray2D(Point2D(0, 0), Point2D(0.71, 0.71)),
         Point2D(0, 3): Ray2D(Point2D(0, 3), Point2D(0.23, 2.0)),
         Point2D(1, 1): Ray2D(Point2D(1, 1), Point2D(0.19, 0.42)),
         Point2D(2, 0): Ray2D(Point2D(2, 0), Point2D(1.1, 0.38))}
        """
        b = {}
        pts = list(p.args)
        pts.append(pts[0])  # close it
        cw = Polygon._isright(*pts[:3])
        if cw:
            pts = list(reversed(pts))
        for v, a in p.angles.items():
            i = pts.index(v)
            p1, p2 = Point._normalize_dimension(pts[i], pts[i + 1])
            ray = Ray(p1, p2).rotate(a/2, v)
            dir = ray.direction
            ray = Ray(ray.p1, ray.p1 + dir/dir.distance((0, 0)))
            if prec is not None:
                ray = Ray(ray.p1, ray.p2.n(prec))
            b[v] = ray
        return b
