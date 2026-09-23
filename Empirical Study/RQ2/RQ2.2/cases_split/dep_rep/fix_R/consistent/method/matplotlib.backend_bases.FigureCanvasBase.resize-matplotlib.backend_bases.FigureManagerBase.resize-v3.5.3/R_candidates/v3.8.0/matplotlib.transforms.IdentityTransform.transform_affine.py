    @_api.rename_parameter("3.8", "points", "values")
    def transform_affine(self, values):
        # docstring inherited
        return np.asanyarray(values)
