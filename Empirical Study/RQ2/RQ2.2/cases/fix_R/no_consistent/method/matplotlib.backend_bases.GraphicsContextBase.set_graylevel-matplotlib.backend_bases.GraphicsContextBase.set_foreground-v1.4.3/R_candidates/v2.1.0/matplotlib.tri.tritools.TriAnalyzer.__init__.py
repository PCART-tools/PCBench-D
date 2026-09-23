    def __init__(self, triangulation):
        if not isinstance(triangulation, Triangulation):
            raise ValueError("Expected a Triangulation object")
        self._triangulation = triangulation
