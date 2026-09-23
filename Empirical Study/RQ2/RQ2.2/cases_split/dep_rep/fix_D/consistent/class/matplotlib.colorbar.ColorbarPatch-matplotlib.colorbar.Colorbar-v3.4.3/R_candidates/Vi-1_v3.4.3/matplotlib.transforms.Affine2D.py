class Affine2D(Affine2DBase):
    """
    A mutable 2D affine transformation.
    """

    def __init__(self, matrix=None, **kwargs):
        """
        Initialize an Affine transform from a 3x3 numpy float array::

          a c e
          b d f
          0 0 1

        If *matrix* is None, initialize with the identity transform.
        """
        super().__init__(**kwargs)
        if matrix is None:
            # A bit faster than np.identity(3).
            matrix = IdentityTransform._mtx.copy()
        self._mtx = matrix.copy()
        self._invalid = 0

    __str__ = _make_str_method("_mtx")

    @staticmethod
    def from_values(a, b, c, d, e, f):
        """
        Create a new Affine2D instance from the given values::

          a c e
          b d f
          0 0 1

        .
        """
        return Affine2D(
            np.array([a, c, e, b, d, f, 0.0, 0.0, 1.0], float).reshape((3, 3)))

    def get_matrix(self):
        """
        Get the underlying transformation matrix as a 3x3 numpy array::

          a c e
          b d f
          0 0 1

        .
        """
        if self._invalid:
            self._inverted = None
            self._invalid = 0
        return self._mtx

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

    def set(self, other):
        """
        Set this transformation from the frozen copy of another
        `Affine2DBase` object.
        """
        _api.check_isinstance(Affine2DBase, other=other)
        self._mtx = other.get_matrix()
        self.invalidate()

    @staticmethod
    def identity():
        """
        Return a new `Affine2D` object that is the identity transform.

        Unless this transform will be mutated later on, consider using
        the faster `IdentityTransform` class instead.
        """
        return Affine2D()

    def clear(self):
        """
        Reset the underlying matrix to the identity transform.
        """
        # A bit faster than np.identity(3).
        self._mtx = IdentityTransform._mtx.copy()
        self.invalidate()
        return self

    def rotate(self, theta):
        """
        Add a rotation (in radians) to this transform in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        a = math.cos(theta)
        b = math.sin(theta)
        rotate_mtx = np.array([[a, -b, 0.0], [b, a, 0.0], [0.0, 0.0, 1.0]],
                              float)
        self._mtx = np.dot(rotate_mtx, self._mtx)
        self.invalidate()
        return self

    def rotate_deg(self, degrees):
        """
        Add a rotation (in degrees) to this transform in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        return self.rotate(math.radians(degrees))

    def rotate_around(self, x, y, theta):
        """
        Add a rotation (in radians) around the point (x, y) in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        return self.translate(-x, -y).rotate(theta).translate(x, y)

    def rotate_deg_around(self, x, y, degrees):
        """
        Add a rotation (in degrees) around the point (x, y) in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        # Cast to float to avoid wraparound issues with uint8's
        x, y = float(x), float(y)
        return self.translate(-x, -y).rotate_deg(degrees).translate(x, y)

    def translate(self, tx, ty):
        """
        Add a translation in place.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        self._mtx[0, 2] += tx
        self._mtx[1, 2] += ty
        self.invalidate()
        return self

    def scale(self, sx, sy=None):
        """
        Add a scale in place.

        If *sy* is None, the same scale is applied in both the *x*- and
        *y*-directions.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        if sy is None:
            sy = sx
        # explicit element-wise scaling is fastest
        self._mtx[0, 0] *= sx
        self._mtx[0, 1] *= sx
        self._mtx[0, 2] *= sx
        self._mtx[1, 0] *= sy
        self._mtx[1, 1] *= sy
        self._mtx[1, 2] *= sy
        self.invalidate()
        return self

    def skew(self, xShear, yShear):
        """
        Add a skew in place.

        *xShear* and *yShear* are the shear angles along the *x*- and
        *y*-axes, respectively, in radians.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        rotX = math.tan(xShear)
        rotY = math.tan(yShear)
        skew_mtx = np.array(
            [[1.0, rotX, 0.0], [rotY, 1.0, 0.0], [0.0, 0.0, 1.0]], float)
        self._mtx = np.dot(skew_mtx, self._mtx)
        self.invalidate()
        return self

    def skew_deg(self, xShear, yShear):
        """
        Add a skew in place.

        *xShear* and *yShear* are the shear angles along the *x*- and
        *y*-axes, respectively, in degrees.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        return self.skew(math.radians(xShear), math.radians(yShear))
