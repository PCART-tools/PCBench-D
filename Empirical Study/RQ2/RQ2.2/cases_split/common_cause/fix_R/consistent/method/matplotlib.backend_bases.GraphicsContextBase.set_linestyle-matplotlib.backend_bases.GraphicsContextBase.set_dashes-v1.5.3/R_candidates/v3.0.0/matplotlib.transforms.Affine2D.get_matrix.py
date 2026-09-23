    def get_matrix(self):
        """
        Get the underlying transformation matrix as a 3x3 numpy array::

          a c e
          b d f
          0 0 1

        .
        """
        self._invalid = 0
        return self._mtx
