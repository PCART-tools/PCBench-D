    def get_matrix(self):
        if self._invalid:
            xt, yt = self._scale_trans.transform_point(self._t)
            self._mtx = np.array([[1.0, 0.0, xt],
                                  [0.0, 1.0, yt],
                                  [0.0, 0.0, 1.0]],
                                 float)
            self._invalid = 0
            self._inverted = None
        return self._mtx
