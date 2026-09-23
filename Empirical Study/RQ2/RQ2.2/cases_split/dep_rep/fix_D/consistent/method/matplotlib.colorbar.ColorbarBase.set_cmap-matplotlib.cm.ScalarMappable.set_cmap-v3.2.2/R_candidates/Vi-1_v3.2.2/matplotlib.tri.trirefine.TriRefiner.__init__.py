    def __init__(self, triangulation):
        cbook._check_isinstance(Triangulation, triangulation=triangulation)
        self._triangulation = triangulation
