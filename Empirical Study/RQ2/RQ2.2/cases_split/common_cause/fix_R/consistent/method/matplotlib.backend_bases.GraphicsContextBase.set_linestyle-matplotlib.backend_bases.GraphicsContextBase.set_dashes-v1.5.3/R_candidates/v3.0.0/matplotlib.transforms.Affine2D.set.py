    def set(self, other):
        """
        Set this transformation from the frozen copy of another
        :class:`Affine2DBase` object.
        """
        if not isinstance(other, Affine2DBase):
            raise ValueError("'other' must be an instance of "
                             "'matplotlib.transform.Affine2DBase'")
        self._mtx = other.get_matrix()
        self.invalidate()
