    def smallest_angle_between(l1, l2):
        """Return the smallest angle formed at the intersection of the
        lines containing the linear entities.

        Parameters
        ==========

        l1 : LinearEntity
        l2 : LinearEntity

        Returns
        =======

        angle : angle in radians

        See Also
        ========

        angle_between, is_perpendicular, Ray2D.closing_angle

        Examples
        ========

        >>> from sympy import Point, Line
        >>> p1, p2, p3 = Point(0, 0), Point(0, 4), Point(2, -2)
        >>> l1, l2 = Line(p1, p2), Line(p1, p3)
        >>> l1.smallest_angle_between(l2)
        pi/4

        See Also
        ========
        angle_between, Ray2D.closing_angle
        """
        if not isinstance(l1, LinearEntity) and not isinstance(l2, LinearEntity):
            raise TypeError('Must pass only LinearEntity objects')

        v1, v2 = l1.direction, l2.direction
        return acos(abs(v1.dot(v2))/(abs(v1)*abs(v2)))
