    @property
    def circumference(self):
        """The circumference of the circle.

        Returns
        =======

        circumference : number or SymPy expression

        Examples
        ========

        >>> from sympy import Point, Circle
        >>> c1 = Circle(Point(3, 4), 6)
        >>> c1.circumference
        12*pi

        """
        return 2 * S.Pi * self.radius
