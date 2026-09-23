    def contains_path(self, path, transform=None):
        """
        Return whether this (closed) path completely contains the given path.

        If *transform* is not ``None``, the path will be transformed before
        checking for containment.
        """
        if transform is not None:
            transform = transform.frozen()
        return _path.path_in_path(self, None, path, transform)
