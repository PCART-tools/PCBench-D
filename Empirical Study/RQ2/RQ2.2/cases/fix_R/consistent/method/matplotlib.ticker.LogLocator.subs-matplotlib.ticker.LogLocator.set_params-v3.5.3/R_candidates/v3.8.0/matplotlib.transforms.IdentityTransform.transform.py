    @_api.rename_parameter("3.8", "points", "values")
    def transform(self, values):
        # docstring inherited
        return np.asanyarray(values)
