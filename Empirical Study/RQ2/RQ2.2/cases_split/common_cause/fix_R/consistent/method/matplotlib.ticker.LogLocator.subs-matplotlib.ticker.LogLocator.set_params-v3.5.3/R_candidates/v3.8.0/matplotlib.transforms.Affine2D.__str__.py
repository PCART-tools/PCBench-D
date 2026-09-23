    def __str__(self):
        return (self._base_str()
                if (self._mtx != np.diag(np.diag(self._mtx))).any()
                else f"Affine2D().scale({self._mtx[0, 0]}, {self._mtx[1, 1]})"
                if self._mtx[0, 0] != self._mtx[1, 1]
                else f"Affine2D().scale({self._mtx[0, 0]})")
