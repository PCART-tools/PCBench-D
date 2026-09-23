    def __init__(self, matrix=None, **kwargs):
        """
        Initialize an Affine transform from a 3x3 numpy float array::

          a c e
          b d f
          0 0 1

        If *matrix* is None, initialize with the identity transform.
        """
        Affine2DBase.__init__(self, **kwargs)
        if matrix is None:
            # A bit faster than np.identity(3).
            matrix = IdentityTransform._mtx.copy()
        self._mtx = matrix.copy()
        self._invalid = 0
