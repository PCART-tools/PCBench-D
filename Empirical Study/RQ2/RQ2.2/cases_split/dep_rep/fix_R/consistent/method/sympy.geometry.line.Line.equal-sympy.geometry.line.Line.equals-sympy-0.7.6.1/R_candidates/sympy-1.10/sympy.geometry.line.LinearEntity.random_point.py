    def random_point(self, seed=None):
        """A random point on a LinearEntity.

        Returns
        =======

        point : Point

        See Also
        ========

        sympy.geometry.point.Point

        Examples
        ========

        >>> from sympy import Point, Line, Ray, Segment
        >>> p1, p2 = Point(0, 0), Point(5, 3)
        >>> line = Line(p1, p2)
        >>> r = line.random_point(seed=42)  # seed value is optional
        >>> r.n(3)
        Point2D(-0.72, -0.432)
        >>> r in line
        True
        >>> Ray(p1, p2).random_point(seed=42).n(3)
        Point2D(0.72, 0.432)
        >>> Segment(p1, p2).random_point(seed=42).n(3)
        Point2D(3.2, 1.92)

        """
        if seed is not None:
            rng = random.Random(seed)
        else:
            rng = random
        t = Dummy()
        pt = self.arbitrary_point(t)
        if isinstance(self, Ray):
            v = abs(rng.gauss(0, 1))
        elif isinstance(self, Segment):
            v = rng.random()
        elif isinstance(self, Line):
            v = rng.gauss(0, 1)
        else:
            raise NotImplementedError('unhandled line type')
        return pt.subs(t, Rational(v))
