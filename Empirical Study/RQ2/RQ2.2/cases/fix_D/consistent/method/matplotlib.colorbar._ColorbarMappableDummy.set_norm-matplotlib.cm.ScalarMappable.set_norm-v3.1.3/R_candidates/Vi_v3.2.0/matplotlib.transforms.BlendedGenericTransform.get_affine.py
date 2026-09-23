    def get_affine(self):
        # docstring inherited
        if self._invalid or self._affine is None:
            if self._x == self._y:
                self._affine = self._x.get_affine()
            else:
                x_mtx = self._x.get_affine().get_matrix()
                y_mtx = self._y.get_affine().get_matrix()
                # This works because we already know the transforms are
                # separable, though normally one would want to set b and
                # c to zero.
                mtx = np.vstack((x_mtx[0], y_mtx[1], [0.0, 0.0, 1.0]))
                self._affine = Affine2D(mtx)
            self._invalid = 0
        return self._affine
