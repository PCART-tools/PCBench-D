    def __init__(self, triangulation):
        from matplotlib import _tri
        super().__init__(triangulation)
        self._cpp_trifinder = _tri.TrapezoidMapTriFinder(
            triangulation.get_cpp_triangulation())
        self._initialize()
