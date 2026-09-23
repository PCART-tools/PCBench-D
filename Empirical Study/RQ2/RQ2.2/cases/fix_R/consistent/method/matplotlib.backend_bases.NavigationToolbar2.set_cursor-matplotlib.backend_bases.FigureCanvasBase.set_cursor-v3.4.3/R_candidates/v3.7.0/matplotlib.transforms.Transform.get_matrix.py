    def get_matrix(self):
        """Get the matrix for the affine part of this transform."""
        return self.get_affine().get_matrix()
