    def __init__(self, triangulation):
        TriFinder.__init__(self, triangulation)
        self._cpp_trifinder = _tri.TrapezoidMapTriFinder(
            triangulation.get_cpp_triangulation())
        self._initialize()
