    @staticmethod
    def affine_rank(*args):
        """The affine rank of a set of points is the dimension
        of the smallest affine space containing all the points.
        For example, if the points lie on a line (and are not all
        the same) their affine rank is 1.  If the points lie on a plane
        but not a line, their affine rank is 2.  By convention, the empty
        set has affine rank -1."""

        if len(args) == 0:
            return -1
        # make sure we're genuinely points
        # and translate every point to the origin
        points = Point._normalize_dimension(*[Point(i) for i in args])
        origin = points[0]
        points = [i - origin for i in points[1:]]

        m = Matrix([i.args for i in points])
        # XXX fragile -- what is a better way?
        return m.rank(iszerofunc = lambda x:
            abs(x.n(2)) < 1e-12 if x.is_number else x.is_zero)
