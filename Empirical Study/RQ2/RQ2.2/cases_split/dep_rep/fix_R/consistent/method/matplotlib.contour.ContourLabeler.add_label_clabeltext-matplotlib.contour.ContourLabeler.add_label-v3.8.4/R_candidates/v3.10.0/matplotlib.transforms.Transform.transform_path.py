    def transform_path(self, path):
        """
        Apply the transform to `.Path` *path*, returning a new `.Path`.

        In some cases, this transform may insert curves into the path
        that began as line segments.
        """
        return self.transform_path_affine(self.transform_path_non_affine(path))
