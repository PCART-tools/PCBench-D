    def reflect(self, line):
        """
        Reflects an object across a line.

        Parameters
        ==========

        line: Line

        Examples
        ========

        >>> from sympy import pi, sqrt, Line, RegularPolygon
        >>> l = Line((0, pi), slope=sqrt(2))
        >>> pent = RegularPolygon((1, 2), 1, 5)
        >>> rpent = pent.reflect(l)
        >>> rpent
        RegularPolygon(Point2D(-2*sqrt(2)*pi/3 - 1/3 + 4*sqrt(2)/3, 2/3 + 2*sqrt(2)/3 + 2*pi/3), -1, 5, -atan(2*sqrt(2)) + 3*pi/5)

        >>> from sympy import pi, Line, Circle, Point
        >>> l = Line((0, pi), slope=1)
        >>> circ = Circle(Point(0, 0), 5)
        >>> rcirc = circ.reflect(l)
        >>> rcirc
        Circle(Point2D(-pi, pi), -5)

        """
        from sympy.geometry.point import Point

        g = self
        l = line
        o = Point(0, 0)
        if l.slope.is_zero:
            y = l.args[0].y
            if not y:  # x-axis
                return g.scale(y=-1)
            reps = [(p, p.translate(y=2*(y - p.y))) for p in g.atoms(Point)]
        elif l.slope is oo:
            x = l.args[0].x
            if not x:  # y-axis
                return g.scale(x=-1)
            reps = [(p, p.translate(x=2*(x - p.x))) for p in g.atoms(Point)]
        else:
            if not hasattr(g, 'reflect') and not all(
                    isinstance(arg, Point) for arg in g.args):
                raise NotImplementedError(
                    'reflect undefined or non-Point args in %s' % g)
            a = atan(l.slope)
            c = l.coefficients
            d = -c[-1]/c[1]  # y-intercept
            # apply the transform to a single point
            x, y = Dummy(), Dummy()
            xf = Point(x, y)
            xf = xf.translate(y=-d).rotate(-a, o).scale(y=-1
                ).rotate(a, o).translate(y=d)
            # replace every point using that transform
            reps = [(p, xf.xreplace({x: p.x, y: p.y})) for p in g.atoms(Point)]
        return g.xreplace(dict(reps))
