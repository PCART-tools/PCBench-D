    def __init__(self, triangulation):
        from matplotlib import _tri
        TriFinder.__init__(self, triangulation)
        self._cpp_trifinder = _tri.TrapezoidMapTriFinder(
            triangulation.get_cpp_triangulation())
        self._initialize()
