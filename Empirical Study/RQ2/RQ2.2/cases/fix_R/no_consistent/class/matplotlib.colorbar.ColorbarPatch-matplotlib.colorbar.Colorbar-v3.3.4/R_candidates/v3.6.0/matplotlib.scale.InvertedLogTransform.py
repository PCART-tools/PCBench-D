class InvertedLogTransform(Transform):
    input_dims = output_dims = 1

    def __init__(self, base):
        super().__init__()
        self.base = base

    def __str__(self):
        return "{}(base={})".format(type(self).__name__, self.base)

    def transform_non_affine(self, a):
        return np.power(self.base, a)

    def inverted(self):
        return LogTransform(self.base)
