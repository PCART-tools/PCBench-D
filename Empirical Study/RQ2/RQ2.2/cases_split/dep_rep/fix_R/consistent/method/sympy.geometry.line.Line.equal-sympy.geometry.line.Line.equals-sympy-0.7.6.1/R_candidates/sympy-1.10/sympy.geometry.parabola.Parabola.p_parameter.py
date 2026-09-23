    @property
    def p_parameter(self):
        """P is a parameter of parabola.

        Returns
        =======

        p : number or symbolic expression

        Notes
        =====

        The absolute value of p is the focal length. The sign on p tells
        which way the parabola faces. Vertical parabolas that open up
        and horizontal that open right, give a positive value for p.
        Vertical parabolas that open down and horizontal that open left,
        give a negative value for p.


        See Also
        ========

        http://www.sparknotes.com/math/precalc/conicsections/section2.rhtml

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))
        >>> p1.p_parameter
        -4

        """
        if self.axis_of_symmetry.slope == 0:
            x = self.directrix.coefficients[2]
            p = sign(self.focus.args[0] + x)
        else:
            y = self.directrix.coefficients[2]
            p = sign(self.focus.args[1] + y)
        return p * self.focal_length
