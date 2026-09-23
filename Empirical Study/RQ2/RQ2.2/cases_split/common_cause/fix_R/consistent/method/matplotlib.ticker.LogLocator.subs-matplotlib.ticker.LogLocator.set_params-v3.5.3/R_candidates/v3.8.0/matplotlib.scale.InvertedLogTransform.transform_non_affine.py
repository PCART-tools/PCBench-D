    @_api.rename_parameter("3.8", "a", "values")
    def transform_non_affine(self, values):
        return np.power(self.base, values)
