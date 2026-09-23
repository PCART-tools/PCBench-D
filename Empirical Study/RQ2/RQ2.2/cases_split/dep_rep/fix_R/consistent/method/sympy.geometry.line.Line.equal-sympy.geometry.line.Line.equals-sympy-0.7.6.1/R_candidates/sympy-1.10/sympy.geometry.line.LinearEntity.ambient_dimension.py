    @property
    def ambient_dimension(self):
        """A property method that returns the dimension of LinearEntity
        object.

        Parameters
        ==========

        p1 : LinearEntity

        Returns
        =======

        dimension : integer

        Examples
        ========

        >>> from sympy import Point, Line
        >>> p1, p2 = Point(0, 0), Point(1, 1)
        >>> l1 = Line(p1, p2)
        >>> l1.ambient_dimension
        2

        >>> from sympy import Point, Line
        >>> p1, p2 = Point(0, 0, 0), Point(1, 1, 1)
        >>> l1 = Line(p1, p2)
        >>> l1.ambient_dimension
        3

        """
        return len(self.p1)
