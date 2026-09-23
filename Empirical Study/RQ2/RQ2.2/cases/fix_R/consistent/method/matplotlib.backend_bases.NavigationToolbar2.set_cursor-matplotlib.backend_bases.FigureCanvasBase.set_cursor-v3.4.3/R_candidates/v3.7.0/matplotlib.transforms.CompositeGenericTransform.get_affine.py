    def get_affine(self):
        # docstring inherited
        if not self._b.is_affine:
            return self._b.get_affine()
        else:
            return Affine2D(np.dot(self._b.get_affine().get_matrix(),
                                   self._a.get_affine().get_matrix()))
