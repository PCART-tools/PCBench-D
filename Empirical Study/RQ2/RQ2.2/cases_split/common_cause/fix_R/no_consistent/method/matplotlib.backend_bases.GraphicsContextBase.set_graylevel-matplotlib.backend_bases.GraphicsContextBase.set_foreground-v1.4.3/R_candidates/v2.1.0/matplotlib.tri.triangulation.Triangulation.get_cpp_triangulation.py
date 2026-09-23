    def get_cpp_triangulation(self):
        # Return the underlying C++ Triangulation object, creating it
        # if necessary.
        if self._cpp_triangulation is None:
            self._cpp_triangulation = _tri.Triangulation(
                self.x, self.y, self.triangles, self.mask, self._edges,
                self._neighbors, not self.is_delaunay)
        return self._cpp_triangulation
