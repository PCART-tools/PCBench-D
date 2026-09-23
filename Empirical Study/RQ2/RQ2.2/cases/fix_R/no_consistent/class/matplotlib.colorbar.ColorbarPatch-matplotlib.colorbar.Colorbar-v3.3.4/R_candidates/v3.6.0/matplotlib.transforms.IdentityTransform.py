class IdentityTransform(Affine2DBase):
    """
    A special class that does one thing, the identity transform, in a
    fast way.
    """
    _mtx = np.identity(3)

    def frozen(self):
        # docstring inherited
        return self

    __str__ = _make_str_method()

    def get_matrix(self):
        # docstring inherited
        return self._mtx

    def transform(self, points):
        # docstring inherited
        return np.asanyarray(points)

    def transform_affine(self, points):
        # docstring inherited
        return np.asanyarray(points)

    def transform_non_affine(self, points):
        # docstring inherited
        return np.asanyarray(points)

    def transform_path(self, path):
        # docstring inherited
        return path

    def transform_path_affine(self, path):
        # docstring inherited
        return path

    def transform_path_non_affine(self, path):
        # docstring inherited
        return path

    def get_affine(self):
        # docstring inherited
        return self

    def inverted(self):
        # docstring inherited
        return self
