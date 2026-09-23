class TriFinder:
    """
    Abstract base class for classes used to find the triangles of a
    Triangulation in which (x, y) points lie.

    Rather than instantiate an object of a class derived from TriFinder, it is
    usually better to use the function `.Triangulation.get_trifinder`.

    Derived classes implement __call__(x, y) where x and y are array-like point
    coordinates of the same shape.
    """

    def __init__(self, triangulation):
        _api.check_isinstance(Triangulation, triangulation=triangulation)
        self._triangulation = triangulation
