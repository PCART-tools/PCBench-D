    def __eq__(self, other):
        if getattr(other, "is_affine", False) and hasattr(other, "get_matrix"):
            return (self.get_matrix() == other.get_matrix()).all()
        return NotImplemented
