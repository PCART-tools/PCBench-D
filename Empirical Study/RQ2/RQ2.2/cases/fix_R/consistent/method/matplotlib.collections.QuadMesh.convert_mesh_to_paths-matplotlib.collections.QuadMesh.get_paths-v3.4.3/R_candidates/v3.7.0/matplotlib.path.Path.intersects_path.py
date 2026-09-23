    def intersects_path(self, other, filled=True):
        """
        Return whether if this path intersects another given path.

        If *filled* is True, then this also returns True if one path completely
        encloses the other (i.e., the paths are treated as filled).
        """
        return _path.path_intersects_path(self, other, filled)
