    def __new__(cls, p1, pt=None, slope=None, **kwargs):
        if isinstance(p1, LinearEntity):
            if pt is not None:
                raise ValueError('When p1 is a LinearEntity, pt should be None')
            p1, pt = Point._normalize_dimension(*p1.args, dim=2)
        else:
            p1 = Point(p1, dim=2)
        if pt is not None and slope is None:
            try:
                p2 = Point(pt, dim=2)
            except (NotImplementedError, TypeError, ValueError):
                raise ValueError(filldedent('''
                    The 2nd argument was not a valid Point.
                    If it was a slope, enter it with keyword "slope".
                    '''))
        elif slope is not None and pt is None:
            slope = sympify(slope)
            if slope.is_finite is False:
                # when infinite slope, don't change x
                dx = 0
                dy = 1
            else:
                # go over 1 up slope
                dx = 1
                dy = slope
            # XXX avoiding simplification by adding to coords directly
            p2 = Point(p1.x + dx, p1.y + dy, evaluate=False)
        else:
            raise ValueError('A 2nd Point or keyword "slope" must be used.')
        return LinearEntity2D.__new__(cls, p1, p2, **kwargs)
