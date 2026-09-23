    def __array__(self, *args, **kwargs):
        """
        Array interface to get at this Transform's affine matrix.
        """
        return self.get_affine().get_matrix()
