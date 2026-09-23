    @property
    def radius(self):
        """The radius of the circle.

        Returns
        =======

        radius : number or SymPy expression

        See Also
        ========

        Ellipse.major, Ellipse.minor, Ellipse.hradius, Ellipse.vradius

        Examples
        ========

        >>> from sympy import Point, Circle
        >>> c1 = Circle(Point(3, 4), 6)
        >>> c1.radius
        6

        """
        return self.args[1]
