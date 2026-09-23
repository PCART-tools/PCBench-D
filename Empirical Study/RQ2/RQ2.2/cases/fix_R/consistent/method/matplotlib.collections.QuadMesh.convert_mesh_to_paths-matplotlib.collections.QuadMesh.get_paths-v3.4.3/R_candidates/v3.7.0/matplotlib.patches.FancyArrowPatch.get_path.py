    def get_path(self):
        """Return the path of the arrow in the data coordinates."""
        # The path is generated in display coordinates, then converted back to
        # data coordinates.
        _path, fillable = self._get_path_in_displaycoord()
        if np.iterable(fillable):
            _path = Path.make_compound_path(*_path)
        return self.get_transform().inverted().transform_path(_path)
