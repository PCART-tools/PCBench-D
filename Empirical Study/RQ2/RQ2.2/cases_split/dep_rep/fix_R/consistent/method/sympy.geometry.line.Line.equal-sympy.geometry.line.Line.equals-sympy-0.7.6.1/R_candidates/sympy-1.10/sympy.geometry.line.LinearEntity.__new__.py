    def __new__(cls, p1, p2=None, **kwargs):
        p1, p2 = Point._normalize_dimension(p1, p2)
        if p1 == p2:
            # sometimes we return a single point if we are not given two unique
            # points. This is done in the specific subclass
            raise ValueError(
                "%s.__new__ requires two unique Points." % cls.__name__)
        if len(p1) != len(p2):
            raise ValueError(
                "%s.__new__ requires two Points of equal dimension." % cls.__name__)

        return GeometryEntity.__new__(cls, p1, p2, **kwargs)
