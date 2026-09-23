    def set(self, other):
        """
        Set this transformation from the frozen copy of another
        `Affine2DBase` object.
        """
        cbook._check_isinstance(Affine2DBase, other=other)
        self._mtx = other.get_matrix()
        self.invalidate()
