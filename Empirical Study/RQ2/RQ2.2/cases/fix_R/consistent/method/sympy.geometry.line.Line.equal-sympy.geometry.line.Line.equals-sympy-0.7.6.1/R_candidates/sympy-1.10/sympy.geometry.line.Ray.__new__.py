    def __new__(cls, p1, p2=None, **kwargs):
        p1 = Point(p1)
        if p2 is not None:
            p1, p2 = Point._normalize_dimension(p1, Point(p2))
        dim = len(p1)

        if dim == 2:
            return Ray2D(p1, p2, **kwargs)
        elif dim == 3:
            return Ray3D(p1, p2, **kwargs)
        return LinearEntity.__new__(cls, p1, p2, **kwargs)
