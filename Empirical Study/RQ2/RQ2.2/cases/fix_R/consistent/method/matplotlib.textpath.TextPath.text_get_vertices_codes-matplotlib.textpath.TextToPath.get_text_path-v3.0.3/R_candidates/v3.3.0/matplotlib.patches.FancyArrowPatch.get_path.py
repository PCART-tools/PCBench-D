    def get_path(self):
        """
        Return the path of the arrow in the data coordinates. Use
        get_path_in_displaycoord() method to retrieve the arrow path
        in display coordinates.
        """
        _path, fillable = self.get_path_in_displaycoord()
        if np.iterable(fillable):
            _path = Path.make_compound_path(*_path)
        return self.get_transform().inverted().transform_path(_path)
