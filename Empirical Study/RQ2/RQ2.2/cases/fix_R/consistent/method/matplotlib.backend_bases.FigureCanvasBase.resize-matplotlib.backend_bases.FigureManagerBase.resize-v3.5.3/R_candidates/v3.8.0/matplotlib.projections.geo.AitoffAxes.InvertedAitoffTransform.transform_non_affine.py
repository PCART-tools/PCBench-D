        @_api.rename_parameter("3.8", "xy", "values")
        def transform_non_affine(self, values):
            # docstring inherited
            # MGDTODO: Math is hard ;(
            return np.full_like(values, np.nan)
