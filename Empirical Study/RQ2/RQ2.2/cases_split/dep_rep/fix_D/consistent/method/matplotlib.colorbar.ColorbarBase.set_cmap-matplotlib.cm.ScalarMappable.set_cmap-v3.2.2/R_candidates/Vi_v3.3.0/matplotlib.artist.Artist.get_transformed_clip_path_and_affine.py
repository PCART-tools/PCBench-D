    def get_transformed_clip_path_and_affine(self):
        """
        Return the clip path with the non-affine part of its
        transformation applied, and the remaining affine part of its
        transformation.
        """
        if self._clippath is not None:
            return self._clippath.get_transformed_path_and_affine()
        return None, None
