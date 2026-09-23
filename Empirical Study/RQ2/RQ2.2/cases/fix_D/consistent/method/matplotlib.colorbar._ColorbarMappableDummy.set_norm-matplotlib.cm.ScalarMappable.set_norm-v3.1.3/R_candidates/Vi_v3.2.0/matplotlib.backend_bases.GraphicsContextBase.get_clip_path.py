    def get_clip_path(self):
        """
        Return the clip path in the form (path, transform), where path
        is a :class:`~matplotlib.path.Path` instance, and transform is
        an affine transform to apply to the path before clipping.
        """
        if self._clippath is not None:
            return self._clippath.get_transformed_path_and_affine()
        return None, None
