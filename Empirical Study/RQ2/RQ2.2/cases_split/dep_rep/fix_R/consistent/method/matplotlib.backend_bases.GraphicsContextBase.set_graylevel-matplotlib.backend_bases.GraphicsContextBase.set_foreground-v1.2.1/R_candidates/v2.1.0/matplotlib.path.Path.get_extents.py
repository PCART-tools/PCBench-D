    def get_extents(self, transform=None):
        """
        Returns the extents (*xmin*, *ymin*, *xmax*, *ymax*) of the
        path.

        Unlike computing the extents on the *vertices* alone, this
        algorithm will take into account the curves and deal with
        control points appropriately.
        """
        from .transforms import Bbox
        path = self
        if transform is not None:
            transform = transform.frozen()
            if not transform.is_affine:
                path = self.transformed(transform)
                transform = None
        return Bbox(_path.get_path_extents(path, transform))
