class AsinhTransform(Transform):
    """Inverse hyperbolic-sine transformation used by `.AsinhScale`"""
    input_dims = output_dims = 1

    def __init__(self, linear_width):
        super().__init__()
        if linear_width <= 0.0:
            raise ValueError("Scale parameter 'linear_width' " +
                             "must be strictly positive")
        self.linear_width = linear_width

    def transform_non_affine(self, a):
        return self.linear_width * np.arcsinh(a / self.linear_width)

    def inverted(self):
        return InvertedAsinhTransform(self.linear_width)
