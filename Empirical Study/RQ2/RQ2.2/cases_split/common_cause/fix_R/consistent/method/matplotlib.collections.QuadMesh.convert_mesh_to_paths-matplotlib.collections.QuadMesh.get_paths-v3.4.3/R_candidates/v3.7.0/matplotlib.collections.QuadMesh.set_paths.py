    def set_paths(self):
        self._paths = self._convert_mesh_to_paths(self._coordinates)
        self.stale = True
