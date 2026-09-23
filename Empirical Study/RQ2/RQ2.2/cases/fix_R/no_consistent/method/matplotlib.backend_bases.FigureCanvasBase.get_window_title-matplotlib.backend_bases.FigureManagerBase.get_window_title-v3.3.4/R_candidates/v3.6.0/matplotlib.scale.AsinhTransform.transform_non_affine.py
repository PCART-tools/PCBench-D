    def transform_non_affine(self, a):
        return self.linear_width * np.arcsinh(a / self.linear_width)
