    def get_path(self):
        """Return the mutated path of the rectangle."""
        _path = self.get_boxstyle()(self._x, self._y,
                                    self._width, self._height,
                                    self.get_mutation_scale(),
                                    self.get_mutation_aspect())
        return _path
