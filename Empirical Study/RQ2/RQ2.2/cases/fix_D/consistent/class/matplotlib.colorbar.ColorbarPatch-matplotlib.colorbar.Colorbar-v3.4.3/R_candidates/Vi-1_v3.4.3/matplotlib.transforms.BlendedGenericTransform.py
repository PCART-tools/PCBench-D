class BlendedGenericTransform(_BlendedMixin, Transform):
    """
    A "blended" transform uses one transform for the *x*-direction, and
    another transform for the *y*-direction.

    This "generic" version can handle any given child transform in the
    *x*- and *y*-directions.
    """
    input_dims = 2
    output_dims = 2
    is_separable = True
    pass_through = True

    def __init__(self, x_transform, y_transform, **kwargs):
        """
        Create a new "blended" transform using *x_transform* to transform the
        *x*-axis and *y_transform* to transform the *y*-axis.

        You will generally not call this constructor directly but use the
        `blended_transform_factory` function instead, which can determine
        automatically which kind of blended transform to create.
        """
        Transform.__init__(self, **kwargs)
        self._x = x_transform
        self._y = y_transform
        self.set_children(x_transform, y_transform)
        self._affine = None

    @property
    def depth(self):
        return max(self._x.depth, self._y.depth)

    def contains_branch(self, other):
        # A blended transform cannot possibly contain a branch from two
        # different transforms.
        return False

    is_affine = property(lambda self: self._x.is_affine and self._y.is_affine)
    has_inverse = property(
        lambda self: self._x.has_inverse and self._y.has_inverse)

    def frozen(self):
        # docstring inherited
        return blended_transform_factory(self._x.frozen(), self._y.frozen())

    def transform_non_affine(self, points):
        # docstring inherited
        if self._x.is_affine and self._y.is_affine:
            return points
        x = self._x
        y = self._y

        if x == y and x.input_dims == 2:
            return x.transform_non_affine(points)

        if x.input_dims == 2:
            x_points = x.transform_non_affine(points)[:, 0:1]
        else:
            x_points = x.transform_non_affine(points[:, 0])
            x_points = x_points.reshape((len(x_points), 1))

        if y.input_dims == 2:
            y_points = y.transform_non_affine(points)[:, 1:]
        else:
            y_points = y.transform_non_affine(points[:, 1])
            y_points = y_points.reshape((len(y_points), 1))

        if (isinstance(x_points, np.ma.MaskedArray) or
                isinstance(y_points, np.ma.MaskedArray)):
            return np.ma.concatenate((x_points, y_points), 1)
        else:
            return np.concatenate((x_points, y_points), 1)

    def inverted(self):
        # docstring inherited
        return BlendedGenericTransform(self._x.inverted(), self._y.inverted())

    def get_affine(self):
        # docstring inherited
        if self._invalid or self._affine is None:
            if self._x == self._y:
                self._affine = self._x.get_affine()
            else:
                x_mtx = self._x.get_affine().get_matrix()
                y_mtx = self._y.get_affine().get_matrix()
                # We already know the transforms are separable, so we can skip
                # setting b and c to zero.
                mtx = np.array([x_mtx[0], y_mtx[1], [0.0, 0.0, 1.0]])
                self._affine = Affine2D(mtx)
            self._invalid = 0
        return self._affine
