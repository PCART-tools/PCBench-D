    def distance(self, o):
        """Distance between the plane and another geometric entity.

        Parameters
        ==========

        Point3D, LinearEntity3D, Plane.

        Returns
        =======

        distance

        Notes
        =====

        This method accepts only 3D entities as it's parameter, but if you want
        to calculate the distance between a 2D entity and a plane you should
        first convert to a 3D entity by projecting onto a desired plane and
        then proceed to calculate the distance.

        Examples
        ========

        >>> from sympy import Point3D, Line3D, Plane
        >>> a = Plane(Point3D(1, 1, 1), normal_vector=(1, 1, 1))
        >>> b = Point3D(1, 2, 3)
        >>> a.distance(b)
        sqrt(3)
        >>> c = Line3D(Point3D(2, 3, 1), Point3D(1, 2, 2))
        >>> a.distance(c)
        0

        """
        if self.intersection(o) != []:
            return S.Zero

        if isinstance(o, (Segment3D, Ray3D)):
            a, b = o.p1, o.p2
            pi, = self.intersection(Line3D(a, b))
            if pi in o:
                return self.distance(pi)
            elif a in Segment3D(pi, b):
                return self.distance(a)
            else:
                assert isinstance(o, Segment3D) is True
                return self.distance(b)

        # following code handles `Point3D`, `LinearEntity3D`, `Plane`
        a = o if isinstance(o, Point3D) else o.p1
        n = Point3D(self.normal_vector).unit
        d = (a - self.p1).dot(n)
        return abs(d)
