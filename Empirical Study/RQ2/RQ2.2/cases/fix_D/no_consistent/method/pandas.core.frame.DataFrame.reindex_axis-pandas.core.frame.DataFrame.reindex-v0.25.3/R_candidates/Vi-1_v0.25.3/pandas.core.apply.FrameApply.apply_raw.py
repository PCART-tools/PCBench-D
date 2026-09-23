    def apply_raw(self):
        """ apply to the values as a numpy array """

        try:
            result = reduction.reduce(self.values, self.f, axis=self.axis)
        except Exception:
            result = np.apply_along_axis(self.f, self.axis, self.values)

        # TODO: mixed type case
        if result.ndim == 2:
            return self.obj._constructor(result, index=self.index, columns=self.columns)
        else:
            return self.obj._constructor_sliced(result, index=self.agg_axis)
