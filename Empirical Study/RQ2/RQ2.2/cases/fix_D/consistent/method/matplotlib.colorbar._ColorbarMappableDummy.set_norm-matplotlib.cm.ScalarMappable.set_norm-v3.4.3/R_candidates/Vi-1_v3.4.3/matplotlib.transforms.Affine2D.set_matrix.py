    def set_matrix(self, mtx):
        """
        Set the underlying transformation matrix from a 3x3 numpy array::

          a c e
          b d f
          0 0 1

        .
        """
        self._mtx = mtx
        self.invalidate()
