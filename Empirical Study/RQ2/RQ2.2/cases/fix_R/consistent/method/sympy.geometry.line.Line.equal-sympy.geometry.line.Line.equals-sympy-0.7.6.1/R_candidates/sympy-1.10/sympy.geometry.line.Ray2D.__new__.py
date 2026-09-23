    def __new__(cls, p1, pt=None, angle=None, **kwargs):
        p1 = Point(p1, dim=2)
        if pt is not None and angle is None:
            try:
                p2 = Point(pt, dim=2)
            except (NotImplementedError, TypeError, ValueError):
                raise ValueError(filldedent('''
                    The 2nd argument was not a valid Point; if
                    it was meant to be an angle it should be
                    given with keyword "angle".'''))
            if p1 == p2:
                raise ValueError('A Ray requires two distinct points.')
        elif angle is not None and pt is None:
            # we need to know if the angle is an odd multiple of pi/2
            c = pi_coeff(sympify(angle))
            p2 = None
            if c is not None:
                if c.is_Rational:
                    if c.q == 2:
                        if c.p == 1:
                            p2 = p1 + Point(0, 1)
                        elif c.p == 3:
                            p2 = p1 + Point(0, -1)
                    elif c.q == 1:
                        if c.p == 0:
                            p2 = p1 + Point(1, 0)
                        elif c.p == 1:
                            p2 = p1 + Point(-1, 0)
                if p2 is None:
                    c *= S.Pi
            else:
                c = angle % (2*S.Pi)
            if not p2:
                m = 2*c/S.Pi
                left = And(1 < m, m < 3)  # is it in quadrant 2 or 3?
                x = Piecewise((-1, left), (Piecewise((0, Eq(m % 1, 0)), (1, True)), True))
                y = Piecewise((-tan(c), left), (Piecewise((1, Eq(m, 1)), (-1, Eq(m, 3)), (tan(c), True)), True))
                p2 = p1 + Point(x, y)
        else:
            raise ValueError('A 2nd point or keyword "angle" must be used.')

        return LinearEntity2D.__new__(cls, p1, p2, **kwargs)
