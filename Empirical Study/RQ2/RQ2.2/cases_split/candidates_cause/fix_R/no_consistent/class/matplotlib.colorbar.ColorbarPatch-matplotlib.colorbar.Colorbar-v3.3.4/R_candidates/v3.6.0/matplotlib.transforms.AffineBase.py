class AffineBase(Transform):
    """
    The base class of all affine transformations of any number of dimensions.
    """
    is_affine = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inverted = None

    def __array__(self, *args, **kwargs):
        # optimises the access of the transform matrix vs. the superclass
        return self.get_matrix()

    def __eq__(self, other):
        if getattr(other, "is_affine", False) and hasattr(other, "get_matrix"):
            return np.all(self.get_matrix() == other.get_matrix())
        return NotImplemented

    def transform(self, values):
        # docstring inherited
        return self.transform_affine(values)

    def transform_affine(self, values):
        # docstring inherited
        raise NotImplementedError('Affine subclasses should override this '
                                  'method.')

    def transform_non_affine(self, points):
        # docstring inherited
        return points

    def transform_path(self, path):
        # docstring inherited
        return self.transform_path_affine(path)

    def transform_path_affine(self, path):
        # docstring inherited
        return Path(self.transform_affine(path.vertices),
                    path.codes, path._interpolation_steps)

    def transform_path_non_affine(self, path):
        # docstring inherited
        return path

    def get_affine(self):
        # docstring inherited
        return self
