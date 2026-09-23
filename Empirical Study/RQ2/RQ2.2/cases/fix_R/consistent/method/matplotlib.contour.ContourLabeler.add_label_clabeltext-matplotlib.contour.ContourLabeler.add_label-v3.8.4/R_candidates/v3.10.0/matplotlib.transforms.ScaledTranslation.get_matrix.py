    def get_matrix(self):
        # docstring inherited
        if self._invalid:
            # A bit faster than np.identity(3).
            self._mtx = IdentityTransform._mtx.copy()
            self._mtx[:2, 2] = self._scale_trans.transform(self._t)
            self._invalid = 0
            self._inverted = None
        return self._mtx
