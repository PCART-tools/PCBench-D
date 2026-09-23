    def __new__(cls, p1, p2, **kwargs):
        p1, p2 = Point._normalize_dimension(Point(p1), Point(p2))
        dim = len(p1)

        if dim == 2:
            return Segment2D(p1, p2, **kwargs)
        elif dim == 3:
            return Segment3D(p1, p2, **kwargs)
        return LinearEntity.__new__(cls, p1, p2, **kwargs)
