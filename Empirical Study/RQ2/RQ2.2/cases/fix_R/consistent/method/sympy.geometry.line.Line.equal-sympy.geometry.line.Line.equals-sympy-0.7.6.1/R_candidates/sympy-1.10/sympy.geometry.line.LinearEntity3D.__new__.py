    def __new__(cls, p1, p2, **kwargs):
        p1 = Point3D(p1, dim=3)
        p2 = Point3D(p2, dim=3)
        if p1 == p2:
            # if it makes sense to return a Point, handle in subclass
            raise ValueError(
                "%s.__new__ requires two unique Points." % cls.__name__)

        return GeometryEntity.__new__(cls, p1, p2, **kwargs)
