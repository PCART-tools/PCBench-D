    def get_matrix(self):
        if self._invalid:
            if self._x == self._y:
                self._mtx = self._x.get_matrix()
            else:
                x_mtx = self._x.get_matrix()
                y_mtx = self._y.get_matrix()
                # This works because we already know the transforms are
                # separable, though normally one would want to set b and
                # c to zero.
                self._mtx = np.vstack((x_mtx[0], y_mtx[1], [0.0, 0.0, 1.0]))
            self._inverted = None
            self._invalid = 0
        return self._mtx
