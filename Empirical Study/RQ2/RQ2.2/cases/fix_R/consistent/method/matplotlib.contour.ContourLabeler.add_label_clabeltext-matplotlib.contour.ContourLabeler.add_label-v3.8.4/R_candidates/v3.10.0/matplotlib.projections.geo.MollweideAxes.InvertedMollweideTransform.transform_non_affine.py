        def transform_non_affine(self, values):
            # docstring inherited
            x, y = values.T
            # from Equations (7, 8) of
            # https://mathworld.wolfram.com/MollweideProjection.html
            theta = np.arcsin(y / np.sqrt(2))
            longitude = (np.pi / (2 * np.sqrt(2))) * x / np.cos(theta)
            latitude = np.arcsin((2 * theta + np.sin(2 * theta)) / np.pi)
            return np.column_stack([longitude, latitude])
