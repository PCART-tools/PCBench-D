    @_api.rename_parameter("3.8", "points", "values")
    def transform_non_affine(self, values):
        # docstring inherited
        if self._x.is_affine and self._y.is_affine:
            return values
        x = self._x
        y = self._y

        if x == y and x.input_dims == 2:
            return x.transform_non_affine(values)

        if x.input_dims == 2:
            x_points = x.transform_non_affine(values)[:, 0:1]
        else:
            x_points = x.transform_non_affine(values[:, 0])
            x_points = x_points.reshape((len(x_points), 1))

        if y.input_dims == 2:
            y_points = y.transform_non_affine(values)[:, 1:]
        else:
            y_points = y.transform_non_affine(values[:, 1])
            y_points = y_points.reshape((len(y_points), 1))

        if (isinstance(x_points, np.ma.MaskedArray) or
                isinstance(y_points, np.ma.MaskedArray)):
            return np.ma.concatenate((x_points, y_points), 1)
        else:
            return np.concatenate((x_points, y_points), 1)
