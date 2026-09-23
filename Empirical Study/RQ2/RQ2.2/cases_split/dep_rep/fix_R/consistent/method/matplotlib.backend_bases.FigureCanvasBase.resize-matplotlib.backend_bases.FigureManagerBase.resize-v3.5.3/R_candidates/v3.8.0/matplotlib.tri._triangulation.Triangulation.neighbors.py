    @property
    def neighbors(self):
        """
        Return integer array of shape (ntri, 3) containing neighbor triangles.

        For each triangle, the indices of the three triangles that
        share the same edges, or -1 if there is no such neighboring
        triangle.  ``neighbors[i, j]`` is the triangle that is the neighbor
        to the edge from point index ``triangles[i, j]`` to point index
        ``triangles[i, (j+1)%3]``.
        """
        if self._neighbors is None:
            self._neighbors = self.get_cpp_triangulation().get_neighbors()
        return self._neighbors
