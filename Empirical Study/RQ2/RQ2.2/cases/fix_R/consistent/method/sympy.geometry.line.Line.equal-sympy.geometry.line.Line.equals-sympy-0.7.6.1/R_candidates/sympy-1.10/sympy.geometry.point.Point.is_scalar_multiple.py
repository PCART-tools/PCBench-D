    def is_scalar_multiple(self, p):
        """Returns whether each coordinate of `self` is a scalar
        multiple of the corresponding coordinate in point p.
        """
        s, o = Point._normalize_dimension(self, Point(p))
        # 2d points happen a lot, so optimize this function call
        if s.ambient_dimension == 2:
            (x1, y1), (x2, y2) = s.args, o.args
            rv = (x1*y2 - x2*y1).equals(0)
            if rv is None:
                raise Undecidable(filldedent(
                    '''Cannot determine if %s is a scalar multiple of
                    %s''' % (s, o)))

        # if the vectors p1 and p2 are linearly dependent, then they must
        # be scalar multiples of each other
        m = Matrix([s.args, o.args])
        return m.rank() < 2
