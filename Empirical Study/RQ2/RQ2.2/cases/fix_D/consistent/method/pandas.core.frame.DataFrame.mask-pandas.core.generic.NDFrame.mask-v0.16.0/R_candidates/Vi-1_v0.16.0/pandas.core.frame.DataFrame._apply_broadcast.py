    def _apply_broadcast(self, func, axis):
        if axis == 0:
            target = self
        elif axis == 1:
            target = self.T
        else:  # pragma: no cover
            raise AssertionError('Axis must be 0 or 1, got %s' % axis)

        result_values = np.empty_like(target.values)
        columns = target.columns
        for i, col in enumerate(columns):
            result_values[:, i] = func(target[col])

        result = self._constructor(result_values, index=target.index,
                                   columns=target.columns)

        if axis == 1:
            result = result.T

        return result
