    def __new__(cls, p1, p2, **kwargs):
        p1 = Point(p1, dim=2)
        p2 = Point(p2, dim=2)

        if p1 == p2:
            return p1

        return LinearEntity2D.__new__(cls, p1, p2, **kwargs)
