class InvertedAsinhTransform(Transform):
    """Hyperbolic sine transformation used by `.AsinhScale`"""
    input_dims = output_dims = 1

    def __init__(self, linear_width):
        super().__init__()
        self.linear_width = linear_width

    def transform_non_affine(self, a):
        return self.linear_width * np.sinh(a / self.linear_width)

    def inverted(self):
        return AsinhTransform(self.linear_width)
