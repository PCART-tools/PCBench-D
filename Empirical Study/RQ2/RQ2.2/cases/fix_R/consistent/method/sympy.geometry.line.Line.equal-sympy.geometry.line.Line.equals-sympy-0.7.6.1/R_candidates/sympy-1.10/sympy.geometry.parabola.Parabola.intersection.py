    def intersection(self, o):
        """The intersection of the parabola and another geometrical entity `o`.

        Parameters
        ==========

        o : GeometryEntity, LinearEntity

        Returns
        =======

        intersection : list of GeometryEntity objects

        Examples
        ========

        >>> from sympy import Parabola, Point, Ellipse, Line, Segment
        >>> p1 = Point(0,0)
        >>> l1 = Line(Point(1, -2), Point(-1,-2))
        >>> parabola1 = Parabola(p1, l1)
        >>> parabola1.intersection(Ellipse(Point(0, 0), 2, 5))
        [Point2D(-2, 0), Point2D(2, 0)]
        >>> parabola1.intersection(Line(Point(-7, 3), Point(12, 3)))
        [Point2D(-4, 3), Point2D(4, 3)]
        >>> parabola1.intersection(Segment((-12, -65), (14, -68)))
        []

        """
        x, y = symbols('x y', real=True)
        parabola_eq = self.equation()
        if isinstance(o, Parabola):
            if o in self:
                return [o]
            else:
                return list(ordered([Point(i) for i in solve([parabola_eq, o.equation()], [x, y])]))
        elif isinstance(o, Point2D):
            if simplify(parabola_eq.subs([(x, o._args[0]), (y, o._args[1])])) == 0:
                return [o]
            else:
                return []
        elif isinstance(o, (Segment2D, Ray2D)):
            result = solve([parabola_eq, Line2D(o.points[0], o.points[1]).equation()], [x, y])
            return list(ordered([Point2D(i) for i in result if i in o]))
        elif isinstance(o, (Line2D, Ellipse)):
            return list(ordered([Point2D(i) for i in solve([parabola_eq, o.equation()], [x, y])]))
        elif isinstance(o, LinearEntity3D):
            raise TypeError('Entity must be two dimensional, not three dimensional')
        else:
            raise TypeError('Wrong type of argument were put')
