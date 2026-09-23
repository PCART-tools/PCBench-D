    def get_fully_transformed_path(self):
        """
        Return a fully-transformed copy of the child path.
        """
        self._revalidate()
        return self._transform.transform_path_affine(self._transformed_path)
