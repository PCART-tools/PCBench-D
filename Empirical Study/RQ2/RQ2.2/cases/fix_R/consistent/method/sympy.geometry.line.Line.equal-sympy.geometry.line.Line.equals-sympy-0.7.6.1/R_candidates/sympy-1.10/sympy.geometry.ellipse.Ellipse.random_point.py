    def random_point(self, seed=None):
        """A random point on the ellipse.

        Returns
        =======

        point : Point

        Examples
        ========

        >>> from sympy import Point, Ellipse
        >>> e1 = Ellipse(Point(0, 0), 3, 2)
        >>> e1.random_point() # gives some random point
        Point2D(...)
        >>> p1 = e1.random_point(seed=0); p1.n(2)
        Point2D(2.1, 1.4)

        Notes
        =====

        When creating a random point, one may simply replace the
        parameter with a random number. When doing so, however, the
        random number should be made a Rational or else the point
        may not test as being in the ellipse:

        >>> from sympy.abc import t
        >>> from sympy import Rational
        >>> arb = e1.arbitrary_point(t); arb
        Point2D(3*cos(t), 2*sin(t))
        >>> arb.subs(t, .1) in e1
        False
        >>> arb.subs(t, Rational(.1)) in e1
        True
        >>> arb.subs(t, Rational('.1')) in e1
        True

        See Also
        ========
        sympy.geometry.point.Point
        arbitrary_point : Returns parameterized point on ellipse
        """
        t = _symbol('t', real=True)
        x, y = self.arbitrary_point(t).args
        # get a random value in [-1, 1) corresponding to cos(t)
        # and confirm that it will test as being in the ellipse
        if seed is not None:
            rng = random.Random(seed)
        else:
            rng = random
        # simplify this now or else the Float will turn s into a Float
        r = Rational(rng.random())
        c = 2*r - 1
        s = sqrt(1 - c**2)
        return Point(x.subs(cos(t), c), y.subs(sin(t), s))
