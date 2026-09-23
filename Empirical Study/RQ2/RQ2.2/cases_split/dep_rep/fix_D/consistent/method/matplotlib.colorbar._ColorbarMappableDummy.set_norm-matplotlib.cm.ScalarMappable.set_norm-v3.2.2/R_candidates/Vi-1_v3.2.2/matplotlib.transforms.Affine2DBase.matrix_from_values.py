    @staticmethod
    @cbook.deprecated(
        "3.2", alternative="Affine2D.from_values(...).get_matrix()")
    def matrix_from_values(a, b, c, d, e, f):
        """
        Create a new transformation matrix as a 3x3 numpy array of the form::

          a c e
          b d f
          0 0 1
        """
        return np.array([[a, c, e], [b, d, f], [0.0, 0.0, 1.0]], float)
