    def closing_angle(r1, r2):
        """Return the angle by which r2 must be rotated so it faces the same
        direction as r1.

        Parameters
        ==========

        r1 : Ray2D
        r2 : Ray2D

        Returns
        =======

        angle : angle in radians (ccw angle is positive)

        See Also
        ========

        LinearEntity.angle_between

        Examples
        ========

        >>> from sympy import Ray, pi
        >>> r1 = Ray((0, 0), (1, 0))
        >>> r2 = r1.rotate(-pi/2)
        >>> angle = r1.closing_angle(r2); angle
        pi/2
        >>> r2.rotate(angle).direction.unit == r1.direction.unit
        True
        >>> r2.closing_angle(r1)
        -pi/2
        """
        if not all(isinstance(r, Ray2D) for r in (r1, r2)):
            # although the direction property is defined for
            # all linear entities, only the Ray is truly a
            # directed object
            raise TypeError('Both arguments must be Ray2D objects.')

        a1 = atan2(*list(reversed(r1.direction.args)))
        a2 = atan2(*list(reversed(r2.direction.args)))
        if a1*a2 < 0:
            a1 = 2*S.Pi + a1 if a1 < 0 else a1
            a2 = 2*S.Pi + a2 if a2 < 0 else a2
        return a1 - a2
