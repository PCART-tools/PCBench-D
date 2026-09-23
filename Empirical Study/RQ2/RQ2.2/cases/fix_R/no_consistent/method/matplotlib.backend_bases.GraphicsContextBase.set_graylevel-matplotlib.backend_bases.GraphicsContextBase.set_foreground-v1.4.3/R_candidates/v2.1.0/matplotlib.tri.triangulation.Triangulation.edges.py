    @property
    def edges(self):
        """
        Return integer array of shape (nedges,2) containing all edges of
        non-masked triangles.

        Each edge is the start point index and end point index.  Each
        edge (start,end and end,start) appears only once.
        """
        if self._edges is None:
            self._edges = self.get_cpp_triangulation().get_edges()
        return self._edges
