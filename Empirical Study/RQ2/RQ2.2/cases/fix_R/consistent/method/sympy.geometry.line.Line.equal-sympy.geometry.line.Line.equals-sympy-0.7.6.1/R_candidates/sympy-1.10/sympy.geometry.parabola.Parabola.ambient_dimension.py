    @property
    def ambient_dimension(self):
        """Returns the ambient dimension of parabola.

        Returns
        =======

        ambient_dimension : integer

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> f1 = Point(0, 0)
        >>> p1 = Parabola(f1, Line(Point(5, 8), Point(7, 8)))
        >>> p1.ambient_dimension
        2

        """
        return 2
