    def transform_path(self, path):
        """
        Returns a transformed path.

        *path*: a :class:`~matplotlib.path.Path` instance.

        In some cases, this transform may insert curves into the path
        that began as line segments.
        """
        return self.transform_path_affine(self.transform_path_non_affine(path))
