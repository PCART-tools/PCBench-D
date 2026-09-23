    def _initialize(self):
        """
        Initialize the underlying C++ object.  Can be called multiple times if,
        for example, the triangulation is modified.
        """
        self._cpp_trifinder.initialize()
