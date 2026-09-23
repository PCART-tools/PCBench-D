    def _apply_raw(self, func, axis):
        try:
            result = lib.reduce(self.values, func, axis=axis)
        except Exception:
            result = np.apply_along_axis(func, axis, self.values)

        # TODO: mixed type case
        if result.ndim == 2:
            return DataFrame(result, index=self.index,
                             columns=self.columns)
        else:
            return Series(result, index=self._get_agg_axis(axis))
