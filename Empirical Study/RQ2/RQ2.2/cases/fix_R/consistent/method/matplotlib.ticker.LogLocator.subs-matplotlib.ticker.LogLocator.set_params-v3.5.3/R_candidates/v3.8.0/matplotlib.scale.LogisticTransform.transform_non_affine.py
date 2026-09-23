    @_api.rename_parameter("3.8", "a", "values")
    def transform_non_affine(self, values):
        """logistic transform (base 10)"""
        return 1.0 / (1 + 10**(-values))
