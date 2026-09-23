    def equation(self, x='x', y='y', _slope=None):
        """
        Returns the equation of an ellipse aligned with the x and y axes;
        when slope is given, the equation returned corresponds to an ellipse
        with a major axis having that slope.

        Parameters
        ==========

        x : str, optional
            Label for the x-axis. Default value is 'x'.
        y : str, optional
            Label for the y-axis. Default value is 'y'.
        _slope : Expr, optional
                The slope of the major axis. Ignored when 'None'.

        Returns
        =======

        equation : SymPy expression

        See Also
        ========

        arbitrary_point : Returns parameterized point on ellipse

        Examples
        ========

        >>> from sympy import Point, Ellipse, pi
        >>> from sympy.abc import x, y
        >>> e1 = Ellipse(Point(1, 0), 3, 2)
        >>> eq1 = e1.equation(x, y); eq1
        y**2/4 + (x/3 - 1/3)**2 - 1
        >>> eq2 = e1.equation(x, y, _slope=1); eq2
        (-x + y + 1)**2/8 + (x + y - 1)**2/18 - 1

        A point on e1 satisfies eq1. Let's use one on the x-axis:

        >>> p1 = e1.center + Point(e1.major, 0)
        >>> assert eq1.subs(x, p1.x).subs(y, p1.y) == 0

        When rotated the same as the rotated ellipse, about the center
        point of the ellipse, it will satisfy the rotated ellipse's
        equation, too:

        >>> r1 = p1.rotate(pi/4, e1.center)
        >>> assert eq2.subs(x, r1.x).subs(y, r1.y) == 0

        References
        ==========

        .. [1] https://math.stackexchange.com/questions/108270/what-is-the-equation-of-an-ellipse-that-is-not-aligned-with-the-axis
        .. [2] https://en.wikipedia.org/wiki/Ellipse#Equation_of_a_shifted_ellipse

        """

        x = _symbol(x, real=True)
        y = _symbol(y, real=True)

        dx = x - self.center.x
        dy = y - self.center.y

        if _slope is not None:
            L = (dy - _slope*dx)**2
            l = (_slope*dy + dx)**2
            h = 1 + _slope**2
            b = h*self.major**2
            a = h*self.minor**2
            return l/b + L/a - 1

        else:
            t1 = (dx/self.hradius)**2
            t2 = (dy/self.vradius)**2
            return t1 + t2 - 1
