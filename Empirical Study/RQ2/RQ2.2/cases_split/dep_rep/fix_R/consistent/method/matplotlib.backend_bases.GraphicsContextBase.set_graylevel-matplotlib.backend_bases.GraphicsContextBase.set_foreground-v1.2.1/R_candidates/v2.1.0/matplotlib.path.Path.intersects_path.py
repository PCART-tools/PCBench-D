    def intersects_path(self, other, filled=True):
        """
        Returns *True* if this path intersects another given path.

        *filled*, when True, treats the paths as if they were filled.
        That is, if one path completely encloses the other,
        :meth:`intersects_path` will return True.
        """
        return _path.path_intersects_path(self, other, filled)
