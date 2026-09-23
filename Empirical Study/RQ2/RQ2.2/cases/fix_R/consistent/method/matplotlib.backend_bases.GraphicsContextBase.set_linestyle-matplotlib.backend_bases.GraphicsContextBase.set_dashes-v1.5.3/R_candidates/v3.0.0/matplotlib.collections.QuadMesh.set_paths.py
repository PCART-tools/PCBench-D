    def set_paths(self):
        self._paths = self.convert_mesh_to_paths(
            self._meshWidth, self._meshHeight, self._coordinates)
        self.stale = True
