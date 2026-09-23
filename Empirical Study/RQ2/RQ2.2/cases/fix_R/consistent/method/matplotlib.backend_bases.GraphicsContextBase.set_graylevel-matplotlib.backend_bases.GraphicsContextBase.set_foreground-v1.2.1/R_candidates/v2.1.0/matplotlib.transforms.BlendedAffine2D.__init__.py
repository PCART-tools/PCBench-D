    def __init__(self, x_transform, y_transform, **kwargs):
        """
        Create a new "blended" transform using *x_transform* to
        transform the *x*-axis and *y_transform* to transform the
        *y*-axis.

        Both *x_transform* and *y_transform* must be 2D affine
        transforms.

        You will generally not call this constructor directly but use
        the :func:`blended_transform_factory` function instead, which
        can determine automatically which kind of blended transform to
        create.
        """
        is_affine = x_transform.is_affine and y_transform.is_affine
        is_separable = x_transform.is_separable and y_transform.is_separable
        is_correct = is_affine and is_separable
        if not is_correct:
            msg = ("Both *x_transform* and *y_transform* must be 2D affine"
                   " transforms.")
            raise ValueError(msg)

        Transform.__init__(self, **kwargs)
        self._x = x_transform
        self._y = y_transform
        self.set_children(x_transform, y_transform)

        Affine2DBase.__init__(self)
        self._mtx = None
