    def equation(self, x='x', y='y'):
        """The equation of the parabola.

        Parameters
        ==========
        x : str, optional
            Label for the x-axis. Default value is 'x'.
        y : str, optional
            Label for the y-axis. Default value is 'y'.

        Returns
        =======
        equation : SymPy expression

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))
        >>> p1.equation()
        -x**2 - 16*y + 64
        >>> p1.equation('f')
        -f**2 - 16*y + 64
        >>> p1.equation(y='z')
        -x**2 - 16*z + 64

        """
        x = _symbol(x, real=True)
        y = _symbol(y, real=True)

        if (self.axis_of_symmetry.slope == 0):
            t1 = 4 * (self.p_parameter) * (x - self.vertex.x)
            t2 = (y - self.vertex.y)**2
        else:
            t1 = 4 * (self.p_parameter) * (y - self.vertex.y)
            t2 = (x - self.vertex.x)**2

        return t1 - t2
