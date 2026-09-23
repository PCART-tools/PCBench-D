    def transform_non_affine(self, values):
        return self.linear_width * np.arcsinh(values / self.linear_width)
