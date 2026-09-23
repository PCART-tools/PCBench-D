    def transform_non_affine(self, a):
        return self.linear_width * np.sinh(a / self.linear_width)
