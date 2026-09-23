    def transform_non_affine(self, values):
        return self.linear_width * np.sinh(values / self.linear_width)
