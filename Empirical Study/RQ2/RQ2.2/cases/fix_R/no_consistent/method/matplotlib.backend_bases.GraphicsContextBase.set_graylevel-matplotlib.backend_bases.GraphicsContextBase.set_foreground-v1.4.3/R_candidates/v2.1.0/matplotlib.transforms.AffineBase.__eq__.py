    def __eq__(self, other):
        if getattr(other, "is_affine", False):
            return np.all(self.get_matrix() == other.get_matrix())
        return NotImplemented
