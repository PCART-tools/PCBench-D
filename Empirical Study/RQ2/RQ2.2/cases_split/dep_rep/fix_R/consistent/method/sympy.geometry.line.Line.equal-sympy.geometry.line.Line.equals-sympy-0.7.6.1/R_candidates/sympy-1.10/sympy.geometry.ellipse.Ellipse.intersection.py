    def intersection(self, o):
        """The intersection of this ellipse and another geometrical entity
        `o`.

        Parameters
        ==========

        o : GeometryEntity

        Returns
        =======

        intersection : list of GeometryEntity objects

        Notes
        -----
        Currently supports intersections with Point, Line, Segment, Ray,
        Circle and Ellipse types.

        See Also
        ========

        sympy.geometry.entity.GeometryEntity

        Examples
        ========

        >>> from sympy import Ellipse, Point, Line
        >>> e = Ellipse(Point(0, 0), 5, 7)
        >>> e.intersection(Point(0, 0))
        []
        >>> e.intersection(Point(5, 0))
        [Point2D(5, 0)]
        >>> e.intersection(Line(Point(0,0), Point(0, 1)))
        [Point2D(0, -7), Point2D(0, 7)]
        >>> e.intersection(Line(Point(5,0), Point(5, 1)))
        [Point2D(5, 0)]
        >>> e.intersection(Line(Point(6,0), Point(6, 1)))
        []
        >>> e = Ellipse(Point(-1, 0), 4, 3)
        >>> e.intersection(Ellipse(Point(1, 0), 4, 3))
        [Point2D(0, -3*sqrt(15)/4), Point2D(0, 3*sqrt(15)/4)]
        >>> e.intersection(Ellipse(Point(5, 0), 4, 3))
        [Point2D(2, -3*sqrt(7)/4), Point2D(2, 3*sqrt(7)/4)]
        >>> e.intersection(Ellipse(Point(100500, 0), 4, 3))
        []
        >>> e.intersection(Ellipse(Point(0, 0), 3, 4))
        [Point2D(3, 0), Point2D(-363/175, -48*sqrt(111)/175), Point2D(-363/175, 48*sqrt(111)/175)]
        >>> e.intersection(Ellipse(Point(-1, 0), 3, 4))
        [Point2D(-17/5, -12/5), Point2D(-17/5, 12/5), Point2D(7/5, -12/5), Point2D(7/5, 12/5)]
        """
        # TODO: Replace solve with nonlinsolve, when nonlinsolve will be able to solve in real domain
        x = Dummy('x', real=True)
        y = Dummy('y', real=True)

        if isinstance(o, Point):
            if o in self:
                return [o]
            else:
                return []

        elif isinstance(o, (Segment2D, Ray2D)):
            ellipse_equation = self.equation(x, y)
            result = solve([ellipse_equation, Line(o.points[0], o.points[1]).equation(x, y)], [x, y])
            return list(ordered([Point(i) for i in result if i in o]))

        elif isinstance(o, Polygon):
            return o.intersection(self)

        elif isinstance(o, (Ellipse, Line2D)):
            if o == self:
                return self
            else:
                ellipse_equation = self.equation(x, y)
                return list(ordered([Point(i) for i in solve([ellipse_equation, o.equation(x, y)], [x, y])]))
        elif isinstance(o, LinearEntity3D):
            raise TypeError('Entity must be two dimensional, not three dimensional')
        else:
            raise TypeError('Intersection not handled for %s' % func_name(o))
