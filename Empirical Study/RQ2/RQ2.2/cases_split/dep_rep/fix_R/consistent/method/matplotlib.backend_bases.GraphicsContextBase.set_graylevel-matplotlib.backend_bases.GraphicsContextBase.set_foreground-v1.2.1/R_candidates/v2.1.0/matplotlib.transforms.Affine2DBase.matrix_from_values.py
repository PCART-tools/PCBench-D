    @staticmethod
    def matrix_from_values(a, b, c, d, e, f):
        """
        (staticmethod) Create a new transformation matrix as a 3x3
        numpy array of the form::

          a c e
          b d f
          0 0 1
        """
        return np.array([[a, c, e], [b, d, f], [0.0, 0.0, 1.0]], float)
