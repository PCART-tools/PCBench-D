    def bisectors(self, other):
        """Returns the perpendicular lines which pass through the intersections
        of self and other that are in the same plane.

        Parameters
        ==========

        line : Line3D

        Returns
        =======

        list: two Line instances

        Examples
        ========

        >>> from sympy import Point3D, Line3D
        >>> r1 = Line3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
        >>> r2 = Line3D(Point3D(0, 0, 0), Point3D(0, 1, 0))
        >>> r1.bisectors(r2)
        [Line3D(Point3D(0, 0, 0), Point3D(1, 1, 0)), Line3D(Point3D(0, 0, 0), Point3D(1, -1, 0))]

        """
        if not isinstance(other, LinearEntity):
            raise GeometryError("Expecting LinearEntity, not %s" % other)

        l1, l2 = self, other

        # make sure dimensions match or else a warning will rise from
        # intersection calculation
        if l1.p1.ambient_dimension != l2.p1.ambient_dimension:
            if isinstance(l1, Line2D):
                l1, l2 = l2, l1
            _, p1 = Point._normalize_dimension(l1.p1, l2.p1, on_morph='ignore')
            _, p2 = Point._normalize_dimension(l1.p2, l2.p2, on_morph='ignore')
            l2 = Line(p1, p2)

        point = intersection(l1, l2)

        # Three cases: Lines may intersect in a point, may be equal or may not intersect.
        if not point:
            raise GeometryError("The lines do not intersect")
        else:
            pt = point[0]
            if isinstance(pt, Line):
                # Intersection is a line because both lines are coincident
                return [self]


        d1 = l1.direction.unit
        d2 = l2.direction.unit

        bis1 = Line(pt, pt + d1 + d2)
        bis2 = Line(pt, pt + d1 - d2)

        return [bis1, bis2]
